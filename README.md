# Ansible Custom Interactive Dynamic Inventory

Custom and interactive inventory for Ansible.

## Purpose

When working with an Ansible dynamic inventory, you may want to update it
from your playbook on the fly. For instance, you may want to create a server and
then install an application on it without calling a second playbook or developing
specific code to create a runtime group (e.g. `add_host` module). Or you may
want to update the inventory on the fly without having to wait for an async mechanism
to be triggered. This all this project is about: providing you a simple, fully
encrypted, interactive dynamic inventory made to measure for your environment.

## Install the backend data model

1. [Install the database](https://siodb.io/getsiodb)
2. Create the inventory data model and the database user:

```bash
git clone git@github.com:siodb/ansible-dynamic-inventory.git
cd ansible-dynamic-inventory
sudo -i -u siodb siocli --user root < sio_inv_data_model.sql
sudo -i -u siodb siocli --user root < sio_inv_user.sql
```

3. Create your groups, groupvars, hosts and hostvars:

```bash
sudo -i -u siodb siocli --user root
```

```sql
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
;

insert into hosts_variables
values
    ( 1, 'public_ip', '0.1.2.3' ),
    ( 1, 'application', 'app01' ),
    ( 2, 'public_ip', '0.1.2.4' ),
    ( 2, 'application', 'app02' ),
    ( 3, 'public_ip', '0.1.2.4' ),
    ( 3, 'application', 'app02' )
;
```

## Configure the inventory

You must tell the inventory script where to lookup for its data. That is done
by configuring the file `sio_inv.ini`:

```ini
[sio_inv]
siodb_rest_ip = localhost
siodb_rest_port = 50443
siodb_rest_user = sioinv
siodb_rest_token = <token-generated-from-scrip-sio_inv_user.sql>
siodb_rest_tls_verify_certificate = no
```

Note: how to generate new token [here](https://docs.siodb.io/authentication/#rest-api-access).

## Validate the inventory

```bash
$ ansible-inventory -i ./sio_inv.py  --graph --vars
@all:
  |--@development:
  |  |--server-03
  |  |  |--{domain_name = company.com}
  |  |  |--{environment_name = development}
  |  |  |--{subnet = 10.30.0.0/16}
  |  |--{environment_name = development}
  |  |--{subnet = 10.30.0.0/16}
  |--@production:
  |  |--hypervisor-01
  |  |  |--{domain_name = company.com}
  |  |  |--{environment_name = production}
  |  |  |--{subnet = 10.10.0.0/16}
  |  |--hypervisor-02
  |  |  |--{domain_name = company.com}
  |  |  |--{environment_name = production}
  |  |  |--{subnet = 10.10.0.0/16}
  |  |--server-01
  |  |  |--{application = app01}
  |  |  |--{domain_name = company.com}
  |  |  |--{environment_name = production}
  |  |  |--{public_ip = 0.1.2.3}
  |  |  |--{subnet = 10.10.0.0/16}
  |  |--server-04
  |  |  |--{domain_name = company.com}
  |  |  |--{environment_name = production}
  |  |  |--{subnet = 10.10.0.0/16}
  |  |--{environment_name = production}
  |  |--{subnet = 10.10.0.0/16}
  |--@test:
  |  |--server-02
  |  |  |--{application = app02}
  |  |  |--{domain_name = company.com}
  |  |  |--{environment_name = test}
  |  |  |--{public_ip = 0.1.2.4}
  |  |  |--{subnet = 10.20.0.0/16}
  |  |--server-05
  |  |  |--{domain_name = company.com}
  |  |  |--{environment_name = test}
  |  |  |--{subnet = 10.20.0.0/16}
  |  |--{environment_name = test}
  |  |--{subnet = 10.20.0.0/16}
  |--@ungrouped:
  |--{domain_name = company.com}
```

## Example of playbook

The file `test_sio_inv.yml` in this repositry is a playbook that demontrate
how to use the custom inventory:

```bash
ansible-playbook -i sio_inv.py test_sio_inv.yml -e vm_name=server-06
```
