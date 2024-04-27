import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "message"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    desk = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("desk.id"))
    thread = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("thread.id"))
    root = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("message.id"), nullable=True)
    writer = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship("User")
    hashed_key = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    number = sqlalchemy.Column(sqlalchemy.Integer)

    def set_key(self, key):
        self.hashed_key = generate_password_hash(key)

    def check_key(self, key):
        return check_password_hash(self.hashed_key, key)
