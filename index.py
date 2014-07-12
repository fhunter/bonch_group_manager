#!/usr/bin/python
# coding=utf-8
import cgi
import cgitb
import pwd
import grp
cgitb.enable()

userbase=u"/selfreg/?page=getuser&getuser="

mainpage=u"""
<h1>Добавление и просмотр групп</h1>
<form method="post" action="" name="groupadd">
Название группы:<input type="text" name="groupname">
Количество студентов:<select name="number">
<option value="50" >50</option>
<option value="40" >40</option>
<option value="30" >30</option>
</select> 
<input type="submit" value="Submit">
</form>
<a href="./?page=listadd">Очередь добавления групп</a><br>
%s

"""

showgrouppage=u"""
<h1>Группа %s</h1>
<table border=1>
%s
</table>
<a href="./?page=mainpage">На главную</a>
"""

queuepage=u"""
<h1>Очередь добавления групп</h1>
<a href="./?page=mainpage">На главную</a>
"""

errorpage=u"""
<h1>Error</h1>
%s
<br>
<a href="./?page=mainpage">На главную</a>
"""

def header_html():
	print "Content-type: text/html"
	print ""

def print_ui(page):
	print """
	<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf8"></head><body>
	"""
	print page.encode('utf-8')
	print """
	</body></html>
	"""

def listadd_ui(form):
	pass

def showgroup_ui(form):
	if "group" in form:
		group=form["group"].value
		try:
			grp.getgrnam(group)
		except:
			print_ui(errorpage % ("No such group 1"))
			return 
		grpvalue = grp.getgrnam(group)
		if ((grpvalue[2] < 1000) or (grpvalue[2] > 64000)):
			print_ui(errorpage % ("No such group 2"))
			return 
		table= u"<tr><td>Группа</td><td>Пользователи</td><td>Комментарий к группе</td></tr>"
		table += u"<tr><td>%s</td>" % (group, )
		table += u"<td>"
  		grptable = u"<table width=\"100%\"><tr>"
		k=0
		for p in grpvalue[3]:
			grptable += "<td width=12.5%><a href=\""+userbase + p +"\">" + unicode(p) + "</a></td>"
			if k%8 == 7:
				grptable += "</tr><tr>"
			k= k+1
		grptable += "</tr></table>"
		table += grptable
		comment = "asdf"
		table += u"</td><td>%s</td></tr>" % (comment, )
		print_ui(showgrouppage % (group,table,))
	else:
		print_ui(errorpage % ("No group specified",))

def mainpage_ui(form):
	table = u"<table border=1><tr><td>Группа</td><td>Пользователи</td><td>Комментарий к группе</td></tr>"
	for i in grp.getgrall():
	  	if (i[2] > 1000) and (i[2] <=64000):
			table += "<tr><td><a href=./?page=showgroup&group=" + unicode(i[0]) + ">" + unicode(i[0]) + "</a></td>"
			k=len(i[3])
			table += u"<td>%d</td>" % k
#	  		table += u"<table width=\"100%\"><tr>"
#			k=0
#			for p in i[3]:
#				table += "<td width=12.5%><a href=\""+userbase + p +"\">" + unicode(p) + "</a></td>"
#				if k%8 == 7:
#					table += "</tr><tr>"
#				k= k+1
#			table += "</tr></table>"
			table += "<td></td></tr>"
	table+="</table>"
	print_ui(mainpage % (table,))
	pass

form = cgi.FieldStorage()

functions = { "listadd": listadd_ui, "showgroup": showgroup_ui, "mainpage": mainpage_ui, }

if "page" in form:
	header_html()
	functions[form["page"].value](form)
	exit(0)

if "listadd" in form:
	header_html()
	print_ui(queuepage)
	exit(0)

header_html()
mainpage_ui(form)
exit(0)
