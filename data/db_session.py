import sqlalchemy as alchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
# from . import __all_models


SqlAlchemyBase = orm.declarative_base()
__factory = None


def global_init(file):
    global __factory
    if __factory:
        return
    engine = alchemy.create_engine(f"sqlite:///{file}?check_same_thread=False", echo=False)
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
