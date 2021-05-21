%include header
<h1>Группы школьников</h1>
<h2>Активные группы</h2>
%include table data=active,buttonscode=''
<hr/>
<h2>На создание</h2>
%include table data=create,buttonscode=''
<hr/>
<h2>На смену пароля</h2>
%include table data=due,buttonscode=''
<hr/>
<h2>Очередь удаления</h2>
%include table data=delete,buttonscode=''
<hr/>
%include menu
%include footer
