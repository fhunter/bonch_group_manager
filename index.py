#!/usr/bin/python
# coding=utf-8
import cgi
import cgitb
import pwd
import grp
cgitb.enable()

userbase=u"/selfreg/?getuser="

mainpage=u"""
<h1>Добавление и просмотр групп</h1>
<form method="get" action="./" name="groupsearch">
Ключ фильтра:<input type="text" name="searchkey">
<input type="submit" value="Submit">
</form>
<form method="post" action="" name="groupadd">
Название группы:<input type="text" name="groupname">
Количество студентов:<select name="number">
<option value="50" >50</option>
<option value="40" >40</option>
<option value="30" >30</option>
</select> 
<input type="submit" value="Submit">
</form>
<a href="./?listadd=html">Очередь добавления групп</a><br>
%s

"""

queuepage=u"""
<h1>Очередь добавления групп</h1>
<a href="./">На главную</a>
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
	<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf8"></head><body>
	"""
	print page.encode('utf-8')
	print """
	</body></html>
	"""

form = cgi.FieldStorage()

if "listadd" in form:
	header_html()
	print_ui(queuepage)
	exit(0)

if "searchkey" in form or 1:
	header_html()
	table = u"<table border=1><tr><td>Группа</td><td>Пользователи</td><td>Комментарий к группе</td></tr>"
	for i in grp.getgrall():
	  	if (i[2] > 1000) and (i[2] <=64000):
			table += "<tr><td>" + unicode(i[0]) + "</td><td>"
	  		table += u"<table width=\"100%\"><tr>"
			k=0
			for p in i[3]:
				table += "<td width=12.5%><a href=\""+userbase + p +"\">" + unicode(p) + "</a></td>"
				if k%8 == 7:
					table += "</tr><tr>"
				k= k+1
			table += "</tr></table>"
			table += "</td></tr>"
	table+="</table>"
	print_ui(mainpage % (table,))
	exit(0)

header_html()
print_ui(mainpage % "")
exit(0)
