----------------------------------------
--- Sample Data set
----------------------------------------
use database sioinv
;

insert into groups
values
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
    ( 2, 'server-01', CURRENT_TIMESTAMP ),
    ( 3, 'server-02', CURRENT_TIMESTAMP ),
    ( 4, 'server-03', CURRENT_TIMESTAMP ),
    ( 2, 'server-04', CURRENT_TIMESTAMP ),
    ( 3, 'server-05', CURRENT_TIMESTAMP ),
    ( 2, 'hypervisor-01', CURRENT_TIMESTAMP ),
    ( 2, 'hypervisor-02', CURRENT_TIMESTAMP )
;

insert into hosts_variables
values
    ( 1, 'public_ip', '0.1.2.3' ),
    ( 1, 'application', 'app01' ),
    ( 2, 'public_ip', '0.1.2.4' ),
    ( 2, 'application', 'app02' )
;
