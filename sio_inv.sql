----------------------------------------
-- User
----------------------------------------

create user sioinv;
alter user sioinv
add token python_inv_script ;

----------------------------------------
-- Data Model
----------------------------------------

use database sys
;
-- drop database sioinv ;
create database sioinv ;
use database sioinv
;

-- Groups table
create table groups
(
    name text
);

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
    name text
);

create table hosts_variables
(
    host_id int,
    name text,
    value text
);

----------------------------------------
--- Sample Data set
----------------------------------------

insert into groups
values
    ( 'all' ),
    ( 'production' ),
    ( 'test' ),
    ( 'development' )
;

insert into groups_variables
values
    ( 1, 'domain_name', 'company.com' ),
    ( 2, 'environment_name', 'production' ),
    ( 2, 'subnet', '10.10.0.0/16' ),
    ( 3, 'environment_name', 'test' ),
    ( 3, 'subnet', '10.20.0.0/16' ),
    ( 4, 'environment_name', 'development' ),
    ( 4, 'subnet', '10.30.0.0/16' )
;

insert into hosts
values
    ( 2, 'server-01' ),
    ( 3, 'server-02' ),
    ( 4, 'server-03' ),
    ( 2, 'server-04' ),
    ( 3, 'server-05' )
;

insert into hosts_variables
values
    ( 1, 'public_ip', '0.1.2.3' ),
    ( 1, 'application', 'app01' ),
    ( 2, 'public_ip', '0.1.2.4' ),
    ( 2, 'application', 'app02' )
;
