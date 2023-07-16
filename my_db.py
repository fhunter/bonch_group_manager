# vim: set fileencoding=utf-8 :
#import secret

""" Database access abstraction module """

import datetime
import enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

def db_exec_sql(*params):
    raise Exception("Not implemented %s" % (params))

class RequestType(enum.Enum):
    STUDENT = 1
    PERSONAL = 2
    TEACHER = 3

class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = relationship("User", back_populates="queue")
    request_type = Column(Enum(RequestType), nullable=False)
    date = Column(DateTime,nullable=False, default=datetime.datetime.now())
    due_date = Column(DateTime,nullable=True, default=None)
    done = Column(Boolean, nullable=False, default=False)
    resetedby = Column(String)

    def __repr__(self):
        return "<Queue(username='%s', password='%s', date='%s' done='%s' resetby='%s')>" % (
                            self.user_id, self.password, self.date, self.done, self.resetedby)

Base.metadata.create_all(engine)
