from data import db_session
from data.user import User


# db_session.global_init("db/base.sqlite")
# session = db_session.create_session()
# print(session.query(User).filter(User.email == "master@gmail.comm").first())
# print(session.query(User).all())
a = {
    1: 1,
    2: 2
}
print(a.get(3))
