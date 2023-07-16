# vim: set fileencoding=utf-8 :
#import secret

""" Database access abstraction module """

import datetime
import enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import sessionmaker

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
    username = Column(String, nullable=False)
    request_type = Column(Enum(RequestType), nullable=False)
    date = Column(DateTime,nullable=False, default=datetime.datetime.now())
    due_date = Column(DateTime,nullable=True, default=None)
    done = Column(Boolean, nullable=False, default=False)
    actedby = Column(String)

    def __repr__(self):
        return "<Queue(username='%s' date='%s' due_date='%s' done='%s' request_type='%s' acted by='%s')>" % (
            self.username,
            self.date,
            self.due_date,
            self.done,
            self.request_type,
            self.actedby)

Base.metadata.create_all(engine)
