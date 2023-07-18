%include('header.tpl')
<h1>Преподаватели</h1>
%include('addform.tpl', action_path='teachers/create')
<hr/>
%include('table.tpl', data=data, actionurl = 'teachers')
<hr/>
%include('footer.tpl')
