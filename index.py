#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

""" Main web app module """
import pwd
import grp
import bottle
from bottle import view, request, response, static_file, abort, redirect
from sqlalchemy import or_, func
import settings
from my_db import Queue, Session
from utils import getcurrentuser, normaliseuser
from utils import require_groups, require_users
from utils import get_users_groups

app = application = bottle.Bottle()

@app.error(403)
def error403(error_m):
    e_message = "<html><head>"
    e_message += f"<meta http-equiv=\"refresh\" content=\"5; url='{settings.PREFIX}/'\" />"
    e_message += "</head><body><h1>Unauthorised, sorry</h1></body></html>"
    return e_message

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

@app.route(settings.PREFIX + '/', method = 'POST')
@require_groups(settings.ADMINGROUPS)
@view('mainpage')
def main_search():
    searchkey = request.forms.getunicode('searchkey')
    userlist=findusers(searchkey)
    return dict(query = userlist)

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

#- TODO: make it so, after debug . Should be available only from 127.0.0.1
@app.route(settings.PREFIX + '/process/newuser', method = 'POST')
@require_users(settings.QUOTAPROCESS)
def receive_users_update():
    """ Method takes in json array of dictionaries: username/password """
    data = request.json
    password = resetpassword(data['username'])
    currentuser = getcurrentuser()
    return dict(username=data['username'],password=password,currentuser=currentuser)

@app.route(settings.PREFIX + r'/<filename:re:.*\.css>')
def send_css(filename):
    #DONE
    return static_file(filename, root='./files/', mimetype='text/css')

@app.route(settings.PREFIX + r'/<filename:re:.*\.js>')
def send_js(filename):
    #DONE
    return static_file(filename, root='./files/', mimetype='text/javascript')

class StripPathMiddleware:
    '''
    Get that slash out of the request
    '''
    def __init__(self, attr):
        self.attr = attr
    def __call__(self, environ, h_data):
        environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')
        return self.a(environ, h_data)

if __name__ == '__main__':
    bottle.run(app=app,
        debug=True, reloader=True,
        host='127.0.0.1',
        port=8888)
