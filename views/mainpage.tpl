%include header
<h1>Группы школьников</h1>
<h2>Активные группы</h2>
% for i in active:
{{ i }} <br/>
% end
<hr/>
<h2>На создание</h2>
% for i in create:
{{ i }} <br/>
% end
<hr/>
<h2>На смену пароля</h2>
% for i in due:
{{ i }} <br/>
% end
<hr/>
<h2>Очередь удаления</h2>
% for i in delete:
{{ i }} <br/>
% end
<hr/>
%include menu
%include footer
