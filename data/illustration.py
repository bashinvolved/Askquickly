import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase


class Illustration(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "illustration"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    message_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("message.id"))
    binary = sqlalchemy.Column(sqlalchemy.String)
