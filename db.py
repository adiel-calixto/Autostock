import sqlalchemy as db
from sqlalchemy.orm import Session, declarative_base

BaseModel = declarative_base()


class DB:
    __conn = None

    @classmethod
    def get_engine(cls):
        if cls.__conn is None:
            cls.__conn = db.create_engine("sqlite:///db.sqlite")

        return cls.__conn

    @classmethod
    def get_session(cls):
        return Session(cls.get_engine())
