import sqlite3


class DB:
    __conn = None

    @classmethod
    def get_conn(cls):
        if cls.__conn is None:
            cls.__conn = sqlite3.connect("app.db")

        return cls.__conn

    @classmethod
    def close_conn(cls):
        if cls.__conn is not None:
            cls.__conn.close()
            cls.__conn = None
