----------------------------------------
-- Data Model
----------------------------------------

use database sys
;
drop database sioinv
;
create database sioinv ;
use database sioinv
;

-- Groups table
create table groups
(
    name text
);

insert into groups
values
    ( 'all' );

create table groups_variables
(
    group_id int,
    name text,
    value text
);

-- Hosts table
create table hosts
(
    group_id int,
    name text,
    creation_timestamp timestamp
        default CURRENT_TIMESTAMP
);

create table hosts_variables
(
    host_id int,
    name text,
    value text
);
