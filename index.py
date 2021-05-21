#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import bottle
from bottle import HTTPError
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.types import DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///test.db', echo=False)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    Base.metadata, # SQLAlchemy metadata, required only if create=True.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

app.install(plugin)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(8), unique=True)
    nrusers = Column(Integer)
    description = Column(String) # Описание группы - цель
    last_reset = Column(DateTime)
    next_reset = Column(Date)
    # Здесь должен быть статус пользователей - логинились или нет
    # И пароли
    responsible = Column(String) # Ответственный преподаватель
    requests = Column(String) # Запросы на права и софт для группы
    issue = Column(String) # Ссылка на issue в gitea

    def __init__(self, name, number=40):
        self.name=name
	self.nrusers=number
    def __repr__(self):
        return "Group(name=%r, users=%r, %s, %s, %s, %s, %s, %s)" % (self.name, self.nrusers, self.description, self.last_reset, self.next_reset, self.responsible, self.requests, self.issue)

class GroupUser(Base):
    __tablename__ = 'groupuser'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(11)) # 8 + 3 (for n[0-9][0-9])
    password = Column(String)
    is_present = Column(Boolean)
    hadlogin = Column(Boolean) # Был ли вход

@app.get('/',sqlalchemy=dict(use_kwargs=True))
@bottle.view('mainpage')
def mainview(db):
    temp_query = db.query(Group)
    active = temp_query
    due = temp_query
    to_delete = temp_query
    create = temp_query
    return {'active':active, 'due': due, 'delete': to_delete, 'create': create }

@app.post('/group/create/<name:re:[a-zA-Z][a-zA-Z0-9]*>/<number:int>')
def groupcreate(name,number,db):
    group=Group(name,number)
    db.add(group)
    db.commit()
    return dict()

@app.get('/group/create/<name:re:[a-zA-Z][a-zA-Z0-9]*>/<number:int>') # FIXME - this is for debug
def groupcreate(name,number,db):
    group=Group(name,number)
    db.add(group)
    db.commit()
    return dict()

@app.delete('/group/delete/<name>')
def groupdelete(name):
    return dict()

@app.get('/group')
def groupget():
    return dict()

@app.get('/group/get/<name>')
def groupgetdetails(name):
    return dict()

@app.post('/group/passwords/<name>')
def group_reset_passwords(name):
    return dict()

@app.get('/group/passwords/<name>')
def group_get_passwords(name):
    return dict()

#@app.get('/:name')
#def show(name, db):
#    entity = db.query(Entity).filter_by(name=name).first()
#    if entity:
#        return {'id': entity.id, 'name': entity.name}
#    return HTTPError(404, 'Entity not found.')

#@app.put('/:name')
#def put_name(name, db):
#    entity = Entity(name)
#    db.add(entity)

#@app.get('/spam/:eggs', sqlalchemy=dict(use_kwargs=True))
#@bottle.view('some_view')
#def route_with_view(eggs, db):
#    pass
#    # do something useful here

app.run(server=bottle.CGIServer)
