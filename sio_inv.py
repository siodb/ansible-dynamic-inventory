#!/bin/python3

import argparse
import os
import six
from six.moves import configparser
import json
import requests
import urllib3

class SioInventoryModule():

    def __init__(self):
        ''' Main execution path '''

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.inventory = {"_meta": {"hostvars": {}}}
        self.siodb_REST_protocol = "https"
        self.siodb_REST_IP = None
        self.siodb_REST_port = None
        self.siodb_REST_user = None
        self.siodb_REST_token = None
        self.siodb_REST_TLS_verify_certificate = None

        # Read settings and parse CLI arguments
        self.parse_cli_args()
        self.read_settings()

        # Build inventory
        self.build_inventory()
        self.print_inventory()

    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(
            description='Produce an Ansible Inventory file from the Siodb Ansible Inventory data model')
        parser.add_argument('--list', action='store_true', default=True,
                            help='List managed nodes (default: True)')
        parser.add_argument('--host', action='store',
                            help='Get all the variables about a specific managed node')
        self.args = parser.parse_args()


    def read_settings(self):
        ''' Reads the settings from the sio_inv.ini file '''

        config = configparser.ConfigParser()
        sio_ini_path = os.environ.get('SIO_INV_INI_PATH',
            os.path.join(os.path.dirname(__file__), 'sio_inv.ini'))
        sio_ini_path = os.path.expanduser(os.path.expandvars(sio_ini_path))

        config.read(sio_ini_path)

        if config.has_option('sio_inv', 'siodb_rest_ip'):
            self.siodb_REST_IP = config.get('sio_inv', 'siodb_rest_ip')
        else:
            self.siodb_REST_IP = "localhost"

        if config.has_option('sio_inv', 'siodb_rest_port'):
            self.siodb_REST_port = config.get('sio_inv', 'siodb_rest_port')
        else:
            self.siodb_REST_port = "50443"

        if config.has_option('sio_inv', 'siodb_rest_user'):
            self.siodb_REST_user = config.get('sio_inv', 'siodb_rest_user')
        else:
            self.siodb_REST_user = "sioinv"

        if config.has_option('sio_inv', 'siodb_rest_token'):
            self.siodb_REST_token = config.get('sio_inv', 'siodb_rest_token')
        else:
            self.siodb_REST_token = none

        if config.has_option('sio_inv', 'siodb_rest_tls_verify_certificate'):
            if config.get('sio_inv', 'siodb_rest_tls_verify_certificate') == "yes":
                self.siodb_REST_TLS_verify_certificate = True
            else:
                self.siodb_REST_TLS_verify_certificate = False
        else:
            self.siodb_REST_TLS_verify_certificate = True


    def get_url(self, table_name):

        url = '{}://{}:{}@{}:{}/databases/sioinv/tables/{}/rows'.format(
                            self.siodb_REST_protocol,
                            self.siodb_REST_user,
                            self.siodb_REST_token,
                            self.siodb_REST_IP,
                            self.siodb_REST_port,
                            table_name
                            )

        response = requests.get(url, verify = self.siodb_REST_TLS_verify_certificate)
        if response.status_code != 200:
            print('ERROR GET {}'.format(response.status_code))

        #print(response.json())

        return response.json()

    def build_inventory(self):

        self.add_group_to_inventory()
        self.add_hosts_to_all()

    def print_inventory(self):

        json_inventory = json.dumps(self.inventory, sort_keys=True)
        print(json_inventory)

    def add_group_to_inventory(self):

        response_json = self.get_url("groups")

        for group in response_json["rows"]:
            self.inventory[group["NAME"]] = { "hosts": [], "vars": {} }
            self.add_vars_to_group(group["TRID"], group["NAME"])
            if group["NAME"].lower() != "all":
                self.add_hosts_to_group(group["TRID"], group["NAME"])

    def add_hosts_to_group(self, group_trid, group_name):

        host_list = []

        response_json = self.get_url("hosts")

        for host in response_json["rows"]:
            #print("{} {} {}".format(host["TRID"], host["GROUP_ID"], host["NAME"]))
            if host["GROUP_ID"] == group_trid:
              host_list.append(host["NAME"])

        if len(host_list) > 0:
            self.inventory[group_name]["hosts"] = host_list

    def add_hosts_to_all(self):

        host_list = []

        response_json = self.get_url("hosts")

        for host in response_json["rows"]:
            #print("{} {} {}".format(host["TRID"], host["GROUP_ID"], host["NAME"]))
            host_list.append(host["NAME"])
            self.add_vars_to_host(host["TRID"], host["NAME"])

        if len(host_list) > 0:
            self.inventory["all"]["hosts"] = host_list

    def add_vars_to_host(self, host_trid, host_name):

        hostvars = {}

        response_json = self.get_url("hosts_variables")

        for hostvar in response_json["rows"]:
            #print("{} {} {}".format(hostvar["TRID"], hostvar["HOST_ID"], hostvar["NAME"], hostvar["VALUE"]))
            if hostvar["HOST_ID"] == host_trid:
                hostvars[hostvar["NAME"]] = hostvar["VALUE"]

        if len(hostvars) > 0 :
            self.inventory["_meta"]["hostvars"][host_name] = hostvars

    def add_vars_to_group(self, group_trid, group_name):

        groupvars = {}

        response_json = self.get_url("groups_variables")

        for groupvar in response_json["rows"]:
            #print("{} {} {} {}".format(groupvar["TRID"], groupvar["GROUP_ID"], groupvar["NAME"], groupvar["VALUE"]))
            if groupvar["GROUP_ID"] == group_trid:
                groupvars[groupvar["NAME"]] = groupvar["VALUE"]

        if len(groupvars) > 0 :
            self.inventory[group_name]["vars"] = groupvars

SioInventoryModule()