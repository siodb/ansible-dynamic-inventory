#!/bin/python3

import argparse
import os
import six
from six.moves import configparser
import json

class InventoryModule():

    def _empty_inventory(self):
        return {"_meta": {"hostvars": {}}}

    def __init__(self):
        ''' Main execution path '''

        self.inventory = self._empty_inventory()

        self.siodb_REST_IP = None
        self.siodb_REST_PORT = None
        self.siodb_REST_USER = None
        self.siodb_REST_TOKEN = None

        # Read settings and parse CLI arguments
        self.parse_cli_args()
        self.read_settings()

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

        print(__file__)
        print(os.path.basename(__file__))

        config = configparser.ConfigParser()
        ec2_ini_path = os.environ.get('SIO_INV_INI_PATH',
            os.path.join(os.path.dirname(__file__), 'sio_inv.ini'))
        ec2_ini_path = os.path.expanduser(os.path.expandvars(ec2_ini_path))

        if not os.path.isfile(ec2_ini_path):
            ec2_ini_path = os.path.expanduser(defaults['ec2']['ini_fallback'])

        config.read(ec2_ini_path)

        if not config.has_option('sio_inv', 'siodb_rest_ip'):
            self.siodb_REST_IP = "localhost"
        if not config.has_option('sio_inv', 'siodb_rest_port'):
            self.siodb_REST_PORT = "50443"
        if not config.has_option('sio_inv', 'siodb_rest_user'):
            self.siodb_REST_USER = "sioinv"
        if not config.has_option('sio_inv', 'siodb_rest_token'):
            self.siodb_REST_TOKEN = none

InventoryModule()