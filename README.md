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

## Get the backend database

1. Clone the data model in the [DataHub](https://datahub.siodb.io/niolap/u3_ansible/clone)
2. Clone the inventory:

```bash
git clone https://github.com/siodb/ansible-dynamic-inventory.git
```

## Configure the inventory

You must tell the inventory script where to lookup for its data your
DataHub API token. You can do this by configuring the file `sio_inv.ini`:

```ini
[sio_inv]
siodb_rest_ip = sdh0001.siodb.io
siodb_rest_port = 50443
siodb_rest_user = niolap
siodb_rest_token = <your-token-from-the-datahub>
siodb_rest_tls_verify_certificate = yes
```

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
