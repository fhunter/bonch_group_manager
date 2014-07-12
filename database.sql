PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE queue (id integer primary key autoincrement, groupame text not null, usernumber integer not null default 40, date datetime not null default current_timestamp, done boolean not null default 'false', addedby text not null);
CREATE TABLE comments(id integer primary key autoincrement, groupname text not null unique, comment text);
COMMIT;
