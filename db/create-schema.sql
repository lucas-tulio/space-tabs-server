create schema spacetabs;

create table iotd_images (
  id int primary key auto_increment,
  link varchar(255) not null);

create table iotd_updates (
  id int primary key auto_increment,
  created_at timestamp default now());
