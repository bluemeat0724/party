from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from datetime import datetime
from contextlib import contextmanager

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

db = SQLAlchemy()

class Base(db.Model):
    __abstract__=True
    create_time = db.Column(db.DateTime,  default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    # status = Column(SmallInteger, default=1)  # 软删除

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        print(item, 'hehe')
        return item