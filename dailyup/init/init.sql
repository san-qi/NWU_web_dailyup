use mysql;
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'qwertyuiop';
flush privileges;
create database test;
use test;
create table user
(
    id varchar(16) unique not null,
    passwd varchar(16) not null,
    active integer not null,
    inSchool integer not null,
    geoInfo json,

    PRIMARY KEY ( `id` )
);
