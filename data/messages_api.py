import flask
import flask_login
import requests
from flask import jsonify, request, render_template
from flask_login import current_user
from . import db_session
from .desk import Desk
from .thread import Thread
from .message import Message
from .user import User
from .illustration import Illustration
from.alert import Alert
from os.path import dirname, realpath
import os


COUNT_OF_MESSAGES = 25


blueprint = flask.Blueprint(
    "messages_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/messages/<string:desk>/<string:thread>/<int:message_identifier>")
def get_conversation(desk, thread, message_identifier):
    session = db_session.create_session()
    desk_id = session.query(Desk).filter(Desk.image_name == desk).first().id
    thread_id = session.query(Thread).filter(Thread.desk_id == desk_id, Thread.image_name == thread).first().id
    messages = (session.query(Message).filter(Message.desk == desk_id, Message.thread == thread_id,
                                              ).all())
    if [elem for elem in messages if elem.id >= message_identifier]:
        messages = [elem for elem in messages if elem.id >= message_identifier]
        messages = messages[:COUNT_OF_MESSAGES]
    else:
        messages = messages[-COUNT_OF_MESSAGES::]
    first_message, last_message = messages[0], messages[-1]
    if first_message.root:
        messages.append(session.query(Message).get(first_message.root))
        messages = [e for e in messages if e.root != first_message.root]
        messages.extend(session.query(Message).filter(Message.root == first_message.root))
    elif last_message.root and first_message.root != last_message.root:
        messages = [e for e in messages if e.root != last_message.root]
        messages.extend(session.query(Message).filter(Message.root == last_message.root))
    messages.sort(key=lambda e: e.id)
    messages = [{
        "id": elem.id,
        "root": elem.root,
        "writer": (us := session.query(User).filter(User.id == elem.writer).first()).name + f" {us.surname}",
        "writer_id": elem.writer,
        "hashed_key": elem.hashed_key,
        "text": elem.text,
        "illustrations": [e.to_dict() for e in session.query(Illustration).filter(Illustration.message_id == elem.id).all()]
    } for elem in messages]
    return jsonify(
        {
            "messages": messages
        }
    )


@blueprint.route("/api/messages/<string:desk>/<string:thread>/total")
def get_total(desk, thread):
    session = db_session.create_session()
    desk_id = session.query(Desk).filter(Desk.image_name == desk).first().id
    thread_id = session.query(Thread).filter(Thread.desk_id == desk_id, Thread.image_name == thread).first().id
    return jsonify(
        {
            "total": session.query(Message.id).filter(Message.desk == desk_id, Message.thread == thread_id).count()
        }
    )


@blueprint.route("/api/messages/<int:message_id>/<string:operation>")
def messages_action(message_id, operation):
    if flask_login.current_user.is_anonymous:
        return flask.redirect('/')
    if operation == "delete":
        session = db_session.create_session()
        message = session.query(Message).get(message_id)
        if message.writer not in [flask_login.current_user.id, 1]:
            return flask.make_response(jsonify({"error": "Forbidden"}), 403)
        prev = session.query(Message).filter(Message.id < message.id, Message.root == None).all()[-1].id
        href = f"{session.query(Desk).get(message.desk).image_name}/{session.query(Thread).get(message.thread).image_name}"
        for elem in session.query(Message).filter(Message.root == message_id):
            for el in session.query(Illustration).filter(Illustration.message_id == elem.id).all():
                os.remove(f"{dirname(realpath(__file__))[:-4]}\\static\\illustration\\{el.id}.png")
            session.delete(elem)
        session.delete(message)
        for elem in session.query(Alert).filter(Alert.message_id == message_id).all():
            session.delete(elem)
        for elem in session.query(Illustration).filter(Illustration.message_id == message_id).all():
            os.remove(f"{dirname(realpath(__file__))[:-4]}\\static\\illustration\\{elem.id}.png")
            session.delete(elem)
        session.commit()
    return flask.redirect(f"/desks/{href}/{prev}")


@blueprint.route("/desks/<string:desk>/<string:thread>/<int:message_identifier>", methods=["POST"])
def post_message(desk, thread, message_identifier):
    if flask_login.current_user.is_anonymous:
        return flask.redirect('/')
    session = db_session.create_session()
    if request.form.get("met") == "put":
        identifier = int(request.form["towhom2"] if request.form.get("towhom2") else request.form["towhom"])
        message = session.query(Message).get(identifier)
        if message.writer not in [flask_login.current_user.id, 1]:
            return flask.make_response(jsonify({"error": "Forbidden"}), 403)
        message.text = request.form["text"]
        if request.form["removements"]:
            for el in set(request.form["removements"].split('|')[:-1]):
                os.remove(f"{dirname(realpath(__file__))[:-4]}\\static\\illustration\\{int(el)}.png")
                session.delete(session.query(Illustration).get(int(el)))
        session.commit()
    elif request.form.get("met") == "key":
        message = session.query(Message).get(int(request.form["identifier"]))
        if message.check_key(request.form["key"]):
            message.writer = flask_login.current_user.id
            session.commit()
        else:
            return flask.make_response(jsonify({"error": "Wrong key"}), 403)
    else:
        message = Message()
        message.thread = session.query(Thread).filter(Thread.image_name == thread).first().id
        message.desk = session.query(Desk).filter(Desk.image_name == desk).first().id
        if request.form.get("towhom", None):
            message.root = request.form["towhom"]
        message.writer = current_user.id
        message.text = request.form["text"]
        if request.form.get("obtainkey", None):
            message.set_key(request.form["obtainkey"])
        session.add(message)
        session.commit()
        if request.form.get("towhom", None):
            if session.query(Message).get(message.root).writer != message.writer:
                alert = Alert()
                alert.message_id = message.id
                alert.user_id = session.query(Message).get(message.root).writer
                session.add(alert)
        if request.form.get("towhom2", None):
            if session.query(Message).get(int(request.form["towhom2"])).writer != message.writer:
                alert = Alert()
                alert.message_id = message.id
                alert.user_id = session.query(Message).get(int(request.form["towhom2"])).writer
                session.add(alert)
    for elem in request.files.getlist("pictures"):
        if not elem.filename:
            continue
        illustration = Illustration()
        illustration.message_id = message.id
        session.add(illustration)
        session.commit()
        f = open(f"{dirname(realpath(__file__))[:-4]}\\static\\illustration\\{illustration.id}.png", "wb")
        f.write(elem.read())
        f.close()
    session.commit()
    return flask.redirect(str(message.id))


@blueprint.route("/desks/<string:desk>/<string:thread>/<int:message_identifier>")
def messages(desk, thread, message_identifier):
    total = requests.get(f"{flask.request.host_url}/api/messages/{desk}/{thread}/total").json()["total"]
    message_identifier = abs(int(message_identifier))
    # if not (1 <= int(message_identifier) <= total):
    #     message_identifier = max(1, min(message_identifier, total))
    #     return flask.redirect(f"{message_identifier}")
    return render_template("messages.html", total=total, title="Обсуждения",
                           current_user=current_user,
                           description=requests
                           .get(f"{flask.request.host_url}/api/messages/{desk}/{thread}/{message_identifier}")
                           .json()["messages"],
                           host=flask.request.host_url, count_of_messages=COUNT_OF_MESSAGES)
