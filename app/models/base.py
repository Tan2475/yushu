from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import SmallInteger, Column, Integer
from contextlib import contextmanager
from datetime import datetime


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            current_app.logger.exception("%r" %e)
            if throw:
                raise e


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    current_time = Column("current_time", Integer)
    status = Column(SmallInteger, default=0)

    def __init__(self):
        self.current_time = int(datetime.now().timestamp())

    def set_attrs(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.current_time:
            return datetime.fromtimestamp(self.current_time)
        else:
            return None
