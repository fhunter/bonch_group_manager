%include header
<h1>Пользователи и группы</h1>
<h2>Студенческие группы</h2>
%include table data=active,buttonscode=''
<hr/>
<h2>Персонал</h2>
%include table data=create,buttonscode=''
<hr/>
<h2>Преподаватели</h2>
%include table data=due,buttonscode=''
<hr/>
<h2>Очередь удаления</h2>
%include table data=delete,buttonscode=''
<hr/>
%include footer
