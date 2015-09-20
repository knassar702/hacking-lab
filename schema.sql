drop table if exists entries;
create table entries (
id INTEGER PRIMARY KEY autoincrement,
title text not null,
description test not null,
text text not null
);