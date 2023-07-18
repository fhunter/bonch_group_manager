
<table border=1>
<tr>
    <th rowspan=2>Имя</th>
    <th rowspan=2>Тип</th>
    <th colspan=2>Дата</th>
    <th rowspan=2>Статус</th>
    <th rowspan=2>От пользователя</th>
    <th rowspan=2>Управление</th>
</tr>
<tr>
<th>Запроса</th>
<th>Выполнения</th>
<tr/>


% for i in data:
<tr>
    <td>{{ i.username }}</td>
    <td>{{ i.request_type }}</td>
    <td>{{ i.date }}</td>
    <td>{{ i.due_date}}</td>
    <td>{{ i.done }}</td>
    <td>{{ i.actedby}}</td>
    <td>
% if i.done:
        <a href={{actionurl}}/delete/{{i.username}}><button>Удалить</button></a>
% else:
        <a href={{actionurl}}/cancel/{{i.username}}><button>Отменить</button></a>
% end
    </td>
</tr>
% end
</table>
