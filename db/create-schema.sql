create schema if not exists spacetabs;
use spacetabs;

drop table if exists iotd_images;
drop table if exists iotd_updates;
drop table if exists log;

create table iotd_images (
  id int primary key auto_increment,
  link varchar(255) not null);

create table iotd_updates (
  id int primary key auto_increment,
  created_at timestamp default now());

create table log (
  id int primary key auto_increment,
  user_ip varchar(255),
  user_agent varchar(255),
  created_at timestamp default now());
