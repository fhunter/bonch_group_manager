%include('header.tpl')
<h1>Студенческие группы</h1>
%include('addform.tpl', action_path='students/create')
<hr/>
%include('table.tpl', data=data, actionurl = 'students')
<hr/>

%include('footer.tpl')
