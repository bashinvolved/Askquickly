import flask
import flask_login
import requests
from flask import jsonify, make_response, render_template
from . import db_session
from .desk import Desk
from .thread import Thread
from .user import User
from .message import Message


blueprint = flask.Blueprint(
    "desks_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/delete/thread/<string:image_name>", methods=["GET"])
def delete_thread(image_name):
    if flask_login.current_user != 1:
        return flask.make_response(jsonify({"error": "Forbidden"}), 403)
    session = db_session.create_session()
    thread = session.query(Thread).filter(Thread.image_name == image_name).first()
    for elem in session.query(Message).filter(Message.thread == thread.id).all():
        session.delete(elem)
    session.delete(thread)
    session.commit()
    return flask.redirect('/')


@blueprint.route("/delete/desk/<string:image_name>", methods=["GET"])
def delete_desk(image_name):
    if flask_login.current_user != 1:
        return flask.make_response(jsonify({"error": "Forbidden"}), 403)
    session = db_session.create_session()
    desk = session.query(Desk).filter(Desk.image_name == image_name).first()
    for elem in session.query(Message).filter(Message.desk == desk.id).all():
        session.delete(elem)
    for elem in session.query(Thread).filter(Thread.desk_id == desk.id).all():
        session.delete(elem)
    session.delete(desk)
    session.commit()
    return flask.redirect('/')


@blueprint.route("/post/desk", methods=["GET"])
def post_desk_form():
    if flask_login.current_user != 1:
        return flask.make_response(jsonify({"error": "Forbidden"}), 403)
    return render_template("postdesk.html")


@blueprint.route("/post/thread", methods=["GET"])
def post_thread_form():
    if flask_login.current_user != 1:
        return flask.make_response(jsonify({"error": "Forbidden"}), 403)
    return render_template("postthread.html")


@blueprint.route("/post/thread", methods=["POST"])
def post_thread():
    if flask_login.current_user != 1:
        return flask.make_response(jsonify({"error": "Forbidden"}), 403)
    session = db_session.create_session()
    thread = Thread()
    thread.desk_id = session.query(Desk).filter(Desk.image_name == flask.request.form["desk_id"]).first().id
    thread.name = flask.request.form["name"]
    thread.image_name = flask.request.form["image_name"]
    session.add(thread)
    session.commit()
    message = Message()
    message.desk = thread.desk_id
    message.thread = thread.id
    message.writer = 1
    message.text = "Начинайте задавать вопросы здесь"
    session.add(message)
    session.commit()
    return flask.redirect('/')


@blueprint.route("/post/desk", methods=["POST"])
def post_desk():
    if flask_login.current_user != 1:
        return flask.make_response(jsonify({"error": "Forbidden"}), 403)
    session = db_session.create_session()
    desk = Desk()
    desk.name = flask.request.form["name"]
    desk.image_name = flask.request.form["image_name"]
    session.add(desk)
    session.commit()
    return flask.redirect("/post/thread")


@blueprint.route("/api/desks")
def get_desks():
    session = db_session.create_session()
    desks = session.query(Desk).all()
    return jsonify(
        {
            "desks": [elem.to_dict(only=("name", "image_name")) for elem in desks]
        }
    )


@blueprint.route("/api/desks/<string:desk>")
def get_threads(desk):
    session = db_session.create_session()
    threads = [elem for elem in session.query(Thread).all() if elem.desk.image_name == desk]
    if not threads:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(
        {
            "threads": [elem.to_dict(only=("name", "image_name")) for elem in threads]
        }
    )


@blueprint.route("/desks")
def desks():
    if flask_login.current_user.is_anonymous:
        session = db_session.create_session()
        flask_login.login_user(session.query(User).get(2), remember=True)
    return render_template("grid.html", title="Доски", start_url="desks/", end_url='',
                           description=requests.get(f"{flask.request.host_url}/api/desks").json()["desks"],
                           host=flask.request.host_url)


@blueprint.route("/desks/<string:desk>")
def threads(desk):
    return render_template("grid.html", title=desk, start_url=f"{desk}/", end_url='/1',
                           description=requests.get(f"{flask.request.host_url}/api/desks/{desk}")
                           .json()["threads"], host=flask.request.host_url)

