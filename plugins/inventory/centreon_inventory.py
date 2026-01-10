# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
    name: centreon_inventory
    short_description: Centreon dynamic inventory source
    description:
        - Fetches hosts from Centreon API v2.
    options:
        protocol:
            description: URL to Centreon API v2.
            required: false
            env:
              - name: CENTREON_PROTOCOL
        hostname:
            description: URL to Centreon API v2.
            required: false
            env:
              - name: CENTREON_HOSTNAME
        port:
            description: URL to Centreon API v2.
            required: false
            env:
              - name: CENTREON_PORT
        path:
            description: URL to Centreon API v2.
            required: false
            env:
              - name: CENTREON_PATH
        username:
            description: Username to Centreon API v2
            required: false
            env:
              - name: CENTREON_USERNAME
        password:
            description: Password to Centreon API v2
            required: false
            env:
              - name: CENTREON_PASSWORD
        token:
            description: Token to Centreon API v2
            required: false
            env:
              - name: CENTREON_TOKEN
        validate_certs:
            description: Whether to validate SSL certificates.
            type: bool
            default: true
            env:
              - name: CENTREON_VALIDATE_CERTS
        timeout:
            description: Timeout for API requests.
            type: int
            default: 30
            env:
              - name: CENTREON_TIMEOUT
'''
import os
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI


class InventoryModule(BaseInventoryPlugin):

    NAME = 'parnoud.centreon.centreon_inventory'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.config = None

    def _get_data(self):
        protocol = self.get_option('protocol') or os.getenv('CENTREON_PROTOCOL') if "protocol" in self.config else False
        hostname = self.get_option('hostname') or os.getenv('CENTREON_HOSTNAME') if "hostname" in self.config else False
        port = self.get_option('port') or os.getenv('CENTREON_PORT') if "port" in self.config else False
        token = self.get_options('token') or os.getenv('CENTREON_TOKEN') if "token" in self.config else False
        username = self.get_option('username') or os.getenv('CENTREON_USERNAME') if "username" in self.config else False
        password = self.get_option('password') or os.getenv('CENTREON_PASSWORD') if "password" in self.config else False
        validate_certs = self.get_option('validate_certs') or os.getenv('CENTREON_VALIDATE_CERTS') if "validate_certs" in self.config else False
        timeout = self.get_option('timeout') or os.getenv('CENTREON_TIMEOUT') if "timeout" in self.config else 30

        try:
            api = CentreonAPI(protocol=protocol, hostname=hostname, port=port, token=token, username=username, password=password, validate_certs=validate_certs, timeout=timeout)
            return api.get_hosts()
        except Exception as e:
            raise AnsibleError(f"Error fetching hosts from Centreon API: {str(e)}")

    def verify_file(self, path):
        if super().verify_file(path):
            if path.endswith(('centreon.yml', 'centreon.yaml')):
                return True
        return False

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self.config = self._read_config_data(path)
        data = self._get_data()
        self._populate(data)

    def _populate(self, data):
        for host in data:
            for group in host['groups']:
                self.inventory.add_group(group['name'])
            self.inventory.add_host(host['name'])
            self.inventory.set_variable(host['name'], "id", host['id'])
            self.inventory.set_variable(host['name'], "alias", host['alias'])
            self.inventory.set_variable(host['name'], "address", host['address'])
