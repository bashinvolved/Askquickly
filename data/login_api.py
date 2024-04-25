import os

import flask
import flask_login
import requests
from flask import render_template, url_for, request, redirect
from . import db_session
from .user import User
from .message import Message
from .alert import Alert
from .desk import Desk
from .thread import Thread

blueprint = flask.Blueprint(
    "login",
    __name__,
    template_folder="templates",
)


@blueprint.route("/logout", methods=["GET", "POST"])
def unregister():
    session = db_session.create_session()
    flask_login.login_user(session.query(User).get(2))
    return redirect('/')


@blueprint.route("/login", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_anonymous:
        return redirect('/')
    if flask_login.current_user.id != 2:
        return flask.redirect(f"/users/{flask_login.current_user.id}")
    warning = False
    if request.method == "POST":
        session = db_session.create_session()
        user = session.query(User).filter(User.email == request.form.get("login")).first()
        if user and user.check_password(request.form.get("password")):
            flask_login.login_user(user, True)
            return redirect(f"/users/{user.id}")
        elif not user:
            user = User()
            user.email = request.form["login"]
            user.set_password(request.form["password"])
            session.add(user)
            session.commit()
            flask_login.login_user(user, True)
            return redirect(f"/users/{user.id}")
        warning = True
    return render_template("login.html", title="Логин", warning=warning)


@blueprint.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    if flask_login.current_user.is_anonymous:
        return redirect('/')
    if not (flask_login.current_user.id == user_id and (user_id not in [1, 2])):
        return flask.make_response(flask.jsonify({"error": "Forbidden"}), 403)
    session = db_session.create_session()
    for elem in session.query(Message).filter(Message.writer == user_id).all():
        requests.get(f"{flask.request.host_url}/api/messages/{elem.id}/delete")
    session.delete(session.query(User).get(user_id))
    session.commit()
    return redirect('/')


@blueprint.route("/users/<int:user_id>/delete/alerts")
def delete_user_alerts(user_id):
    if flask_login.current_user.is_anonymous:
        return redirect('/')
    if not (flask_login.current_user.id == user_id and user_id != 2):
        return flask.make_response(flask.jsonify({"error": "Forbidden"}), 403)
    session = db_session.create_session()
    for elem in session.query(Alert).filter(Alert.user_id == flask_login.current_user.id).all():
        session.delete(elem)
    session.commit()
    return redirect(f"/users/{user_id}")


@blueprint.route("/users/<int:user_id>", methods=["GET", "POST"])
def profile(user_id):
    if flask_login.current_user.is_anonymous:
        return redirect('/')
    warning = False
    session = db_session.create_session()
    if request.method == "POST":
        if user_id not in [flask_login.current_user.id, 1]:
            return flask.make_response(flask.jsonify({"error": "Forbidden"}), 403)
        user = session.query(User).get(user_id)
        if request.form.get("name"):
            user.name = request.form.get("name")
        if request.form.get("surname"):
            user.surname = request.form.get("surname")
        if request.form.get("login"):
            if (request.form.get("login"),) in session.query(User.email).all():
                warning = True
            else:
                user.email = request.form.get("login")
        if request.form.get("password"):
            user.set_password(request.form.get("password"))
        user.disclose_questions = not bool(request.form.get("messages"))
        user.disclose_answers = not bool(request.form.get("alerts"))
        session.commit()
    messages, alerts = list(), list()
    user = session.query(User).get(user_id)
    if user.disclose_questions or flask_login.current_user.id == user.id:
        messages = session.query(Message).filter(Message.writer == user.id).all()
        messages = [{
            "id": elem.id,
            "desk": session.query(Desk).get(elem.desk).image_name,
            "thread": session.query(Thread).get(elem.thread).image_name,
        } for elem in messages]
    if user.disclose_answers or flask_login.current_user.id == user.id:
        alerts = session.query(Alert).filter(Alert.user_id == user.id).all()
        alerts = [{
            "id": elem.message_id,
            "desk": session.query(Desk).get(session.query(Message).get(elem.message_id).desk).image_name,
            "thread": session.query(Thread).get(session.query(Message).get(elem.message_id).thread).image_name,
        } for elem in alerts]
    return render_template("profile.html", title="Профиль",
                           alerts=alerts, messages=messages, form_is_displayed=(flask_login.current_user.id in (user_id, 1)),
                           name=user.name, surname=user.surname, warning=warning)



