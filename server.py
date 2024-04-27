import os

import flask_login
from flask import Flask, make_response, jsonify, redirect, render_template
from flask_login import LoginManager
from data import db_session, desks_api, messages_api, login_api
from data.user import User

application = Flask(__name__)
application.config["SECRET_KEY"] = "abfjfhjueWH7DHJdshjs5ajDHjjdhj4dfsjKFDjdsk"
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@application.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


@application.route("/about")
def ab():
    return render_template("about.html", title="О проекте")


@application.route("/instructions")
def instructions():
    return render_template("instructions.html", title="Документация")


@application.route('/')
def index():
    return redirect("/desks")


def main():
    login_manager.init_app(application)
    login_manager.login_view = "login"
    db_session.global_init("db/base.sqlite")
    for elem in [
        desks_api.blueprint, login_api.blueprint,
        messages_api.blueprint
    ]:
        application.register_blueprint(elem)
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
