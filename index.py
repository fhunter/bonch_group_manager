#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

""" Main web app module """
import re
import pwd
import grp
import bottle
from bottle import view, request, response, static_file, abort, redirect
from sqlalchemy import or_, func
import settings
from my_db import AddQueue, DelQueue, Session, RequestType
from utils import getcurrentuser, normaliseuser
from utils import require_groups, require_users
from utils import get_users_groups
from utils import AttrDict

app = application = bottle.Bottle()

def list2queue(lst, request_type):
    lst2 = []
    for i in lst:
        tmp = AttrDict()
        tmp['username'] = i
        tmp['request_type'] = request_type
        tmp['date'] = None
        tmp['due_date'] = None
        tmp['done'] = True
        tmp['actedby'] = None
        lst2.append(tmp)
    return lst2

@app.error(403)
def error403(error_m):
    e_message = "<html><head>"
    e_message += f"<meta http-equiv=\"refresh\" content=\"5; url='{settings.PREFIX}/'\" />"
    e_message += "</head><body><h1>Unauthorised, sorry</h1></body></html>"
    return e_message

@app.get('/')
@bottle.view('mainpage')
def mainview():
    return dict()

@app.get('/students')
@bottle.view('students')
def studentsview():
    students_group = grp.getgrnam(settings.STUDENT_GROUP).gr_gid
    groups = list(set([re.sub(r'n[0-9][0-9]$','',i.pw_name)  for i in pwd.getpwall() if (i.pw_gid==students_group) and (i.pw_uid>=1000)]))
    groups = list2queue(groups, RequestType.STUDENTS)
# FIXME: smart join
    s = Session()
    groups2 = s.query(AddQueue).filter(AddQueue.request_type == RequestType.STUDENTS).all()
    return dict(data = groups2 + groups)

@app.get('/teachers')
@bottle.view('teachers')
def teachersview():
    teachers_group = grp.getgrnam(settings.TEACHERS_GROUP).gr_gid
    groups = list(set([i.pw_name for i in pwd.getpwall() if (i.pw_gid==teachers_group) and (i.pw_uid>=1000)]))
    groups = list2queue(groups, RequestType.TEACHERS)
# FIXME: smart join
    s = Session()
    groups2 = s.query(AddQueue).filter(AddQueue.request_type == RequestType.TEACHERS).all()
    return dict(data = groups2 + groups)

@app.get('/personal')
@bottle.view('personal')
def personalview():
    personal_group = grp.getgrnam(settings.PERSONAL_GROUP).gr_gid
    groups = list(set([i.pw_name for i in pwd.getpwall() if (i.pw_gid==personal_group) and (i.pw_uid>=1000)]))
    groups = list2queue(groups, RequestType.PERSONAL)
# FIXME: smart join
    s = Session()
    groups2 = s.query(AddQueue).filter(AddQueue.request_type == RequestType.PERSONAL).all()
    return dict(data = groups2 + groups)

@app.get('/statistics')
@bottle.view('statistics')
def statisticsview():
    return dict()

@app.get('/queue')
@bottle.view('queue')
def queueview():
    s = Session()
    add_queue = s.query(AddQueue).all()
    del_queue = s.query(DelQueue).all()
    return dict(add_queue= add_queue, del_queue = del_queue)

# API start
@app.post('/<datatype:re:(students|personal|teachers)>/create/')
def request_create(datatype):
    name = request.params['name']
# FIXME: add checks here
    t = AddQueue(username=name, request_type = datatype.upper() )
    s = Session()
    s.add(t)
    s.commit()
    print(name)
    redirect(f'/{datatype}')

@app.route('/<datatype:re:(students|personal|teachers)>/delete/<name:re:[a-zA-Z][a-zA-Z0-9]*>')
def request_delete(datatype,name):
# FIXME: add checks here
    s = Session()
    t = DelQueue(username = name, request_type = datatype.upper())
    s.add(t)
    s.commit()
    redirect(f'/{datatype}')

@app.route('/<datatype:re:(students|personal|teachers)>/cancel/<name:re:[a-zA-Z][a-zA-Z0-9]*>')
def request_cancel(datatype,name):
    s = Session()
# FIXME: add checks here
    result = s.query(AddQueue).filter(AddQueue.username == name).filter(AddQueue.request_type == datatype.upper()).filter(done == False).all()
    for i in result:
        s.delete(i)
    s.commit()
    redirect(f'/{datatype}')

@app.route('/<datatype:re:(addqueue|delqueue)>/cancel/<name:re:[a-zA-Z][a-zA-Z0-9]*>')
def request_queue_cancel(datatype,name):
    s = Session()
# FIXME: add checks here
    result = []
    if datatype == "addqueue":
        result = s.query(AddQueue).filter(AddQueue.username == name).filter(AddQueue.done == False).all()
    elif datatype == "delqueue":
        result = s.query(DelQueue).filter(DelQueue.username == name).filter(DelQueue.done == False).all()
    for i in result:
        s.delete(i)
    s.commit()
    redirect('/queue')

#@app.route(settings.PREFIX + '/', method = 'POST')
#@require_groups(settings.ADMINGROUPS)
#@view('mainpage')
#def main_search():
#    searchkey = request.forms.getunicode('searchkey')
#    userlist=findusers(searchkey)
#    return dict(query = userlist)

##- TODO: make it so, after debug . Should be available only from 127.0.0.1
#@app.route(settings.PREFIX + '/process/newuser', method = 'POST')
#@require_users(settings.QUOTAPROCESS)
#def receive_users_update():
#    """ Method takes in json array of dictionaries: username/password """
#    data = request.json
#    password = resetpassword(data['username'])
#    currentuser = getcurrentuser()
#    return dict(username=data['username'],password=password,currentuser=currentuser)

# css and javascript processing
@app.route(settings.PREFIX + r'/<filename:re:.*\.css>')
def send_css(filename):
    #DONE
    return static_file(filename, root='./files/', mimetype='text/css')

@app.route(settings.PREFIX + r'/<filename:re:.*\.js>')
def send_js(filename):
    #DONE
    return static_file(filename, root='./files/', mimetype='text/javascript')

if __name__ == '__main__':
    bottle.run(app=app,
        debug=True, reloader=True,
        host='127.0.0.1',
        port=8888)
