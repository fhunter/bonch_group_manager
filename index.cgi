#!/usr/bin/python
# coding=utf-8
import cgi
import cgitb
import pwd
import grp
cgitb.enable()

mainpage=u"""
<h1>Добавление и просмотр групп</h1>
<form method="get" action="./" name="groupsearch">
Ключ фильтра:<input type="text" name="searchkey">
<input type="submit" value="Submit">
</form>
%s
<br>
<a href="./?listadd=html">Очередь добавления групп</a>
"""

errorpage=u"""
<h1>Error</h1>
%s
"""

def header_html():
	print "Content-type: text/html"
	print ""

def print_ui(page):
	print """
	<html><meta http-equiv="Content-Type" content="text/html;charset=utf8"><head></head><body>
	"""
	print page.encode('utf-8')
	print """
	</body></html>
	"""

form = cgi.FieldStorage()

if "searchkey" in form:
	header_html()
	table = u"<table><tr><td>Группа</td><td>Пользователи</td></tr>"
	for i in grp.getgrall():
	  	if (i[2] > 1000) and (i[2] <=64000):
			table += "<tr><td>" + unicode(i[0]) + "</td><td>"
			for p in i[3]:
				#FIXME: add links to user info
				table += unicode(p) + " "
			table += "</td></tr>"
	table+="</table>"
	print_ui(mainpage % (table,))
	exit(0)

header_html()
print_ui(mainpage % "")
exit(0)
