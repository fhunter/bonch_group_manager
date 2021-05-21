
<table border=1>
<tr>
    <th rowspan=2>Имя</th>
    <th rowspan=2>Количество</th>
    <th rowspan=2>Описание</th>
    <th colspan=2>Пароль</th>
    <th rowspan=2>Ответственный за группу</th>
    <th rowspan=2>Информация о требованиях по софту</th>
    <th rowspan=2>Ссылка на требования в gitea</th>
<th></th>
</tr>
<tr>
    <th>Последний сброс</th>
    <th>Следующий сброс</th>
</tr>
</tr>

% for i in data:
<tr>
    <td>{{ i.name }}</td>
    <td>{{ i.nrusers }}</td>
    <td>{{ i.description }}</td>
    <td>{{ i.last_reset }}</td>
    <td>{{ i.next_reset }}</td>
    <td>{{ i.responsible }}</td>
    <td>{{ i.requests }}</td>
    <td>{{ i.issue }}</td>
    <td>{{ buttonscode }}</td>
</tr>
% end
</table>
