import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Desk(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "desk"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    image_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
