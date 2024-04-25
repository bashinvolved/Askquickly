import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Thread(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "thread"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    desk_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("desk.id"))
    desk = orm.relationship("Desk")
    name = sqlalchemy.Column(sqlalchemy.String)
    image_name = sqlalchemy.Column(sqlalchemy.String, unique=True)
