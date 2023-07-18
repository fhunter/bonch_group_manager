%include('header.tpl')
<h1>Персонал</h1>
%include('addform.tpl', action_path='personal/create')
<hr/>
%include('table.tpl', data=data, actionurl = 'personal')
<hr/>
%include('footer.tpl')
