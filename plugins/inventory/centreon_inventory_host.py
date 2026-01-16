# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
    name: centreon_inventory_host
    short_description: Centreon host inventory source
    author:
        - ARNOUD Pierre (@parnoud)
    description:
        - Get Centreon host as inventory hosts
        - Uses any file which ends with centreon.yml or centreon.yaml as YAML configuration file.
    options:
        hostname:
            description: URL to Centreon API v2.
            required: true
            env:
                - name: CENTREON_HOSTNAME
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
            default: false
            env:
                - name: CENTREON_VALIDATE_CERTS
        timeout:
            description: Timeout for API requests.
            type: int
            default: 30
            env:
                - name: CENTREON_TIMEOUT
        search:
            description: search criteria for fetching hosts (list or dict).
            required: false
        attributes:
            description:
                - attributes to include in the inventory.
                - default add all attributes and groups by templates, groups and categories
                - templates (cetreon host templates) listed as list_templates
                - groups (cetreon host groups) listed as list_groups
                - categories (centreon host categories) listed as list_categories
            type: list
            required: false
            elements: str
            default:
                - monitoring_server
                - templates
                - normal_check_interval
                - retry_check_interval
                - check_timeperiod
                - severity
                - categories
                - groups
                - is_activated
'''

EXAMPLES = r"""
# Sample configuration file for Centreon Host dynamic inventory
    plugin: parnoud.centreon.centreon_inventory_host
    hostname: http://centreon.local/centreon/api/latest
    username: username
    password: password

# Sample configuration file for Centreon Host dynamic inventory with select attributes
    plugin: parnoud.centreon.centreon_inventory_host
    hostname: http://centreon.local/centreon/api/latest
    username: username
    password: password
    attributes:
        - templates

# Sample configuration file Centreon Host dynamic inventory using search filter
    plugin: parnoud.centreon.centreon_inventory_host
    hostname: http://centreon.home/centreon/api/latest
    username: username
    password: password
    search:
    "$or":
        - "name":
            "$lk": "server-%"
        - "name":
            "$lk": "switch-%"
"""

import json
import os

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.host import find_all_host_configuration


class InventoryModule(BaseInventoryPlugin):

    NAME = 'parnoud.centreon.centreon_inventory_host'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.config = None

    def _get_data(self):
        hostname = self.get_option('hostname') or os.getenv('CENTREON_HOSTNAME')
        token = self.get_option('token') or os.getenv('CENTREON_TOKEN')
        username = self.get_option('username') or os.getenv('CENTREON_USERNAME')
        password = self.get_option('password') or os.getenv('CENTREON_PASSWORD')
        validate_certs = self.get_option('validate_certs') or os.getenv('CENTREON_VALIDATE_CERTS')
        timeout = self.get_option('timeout') or os.getenv('CENTREON_TIMEOUT')
        search_criteria = self.get_option('search') or None

        if token == '':
            token = None
        if username == '':
            username = None
        if password == '':
            password = None
        filter_criteria = None
        if search_criteria:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps(search_criteria)
        try:
            api = CentreonAPI(hostname=hostname,
                              token=token,
                              username=username,
                              password=password,
                              validate_certs=validate_certs,
                              timeout=timeout)

            result = find_all_host_configuration(api, params=filter_criteria)
            if len(result) >= 1:
                return result
            else:
                raise AnsibleError(f"No result found with search value: {filter_criteria}")
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
        attributes = self.get_option('attributes') or []
        for host in data:
            self.inventory.add_host(host['name'])

            for group in host['groups']:
                self.inventory.add_group('groups')
                self.inventory.add_group(group['name'])
                self.inventory.add_child('groups', group['name'])
                self.inventory.add_child(group['name'], host['name'])

            if 'templates' in attributes or len(attributes) == 0:
                for template in host['templates']:
                    self.inventory.add_group('templates')
                    self.inventory.add_group(template['name'])
                    self.inventory.add_child('templates', template['name'])
                    self.inventory.add_child(template['name'], host['name'])

            if 'categories' in attributes or len(attributes) == 0:
                for categorie in host['categories']:
                    self.inventory.add_group('categories')
                    self.inventory.add_group(categorie['name'])
                    self.inventory.add_child('categories', categorie['name'])
                    self.inventory.add_child(categorie['name'], host['name'])

            self.inventory.set_variable(host['name'], "id", host['id'])
            self.inventory.set_variable(host['name'], "alias", host['alias'])
            self.inventory.set_variable(host['name'], "address", host['address'])
            self.inventory.set_variable(host['name'], "monitoring_server", host['monitoring_server'])

            if 'templates' in attributes or len(attributes) == 0:
                self.inventory.set_variable(host['name'], "list_templates", host['templates'])
            if 'normal_check_interval' in attributes or len(attributes) == 0:
                self.inventory.set_variable(host['name'], "normal_check_interval", host['normal_check_interval'])
            if 'retry_check_interval' in attributes or len(attributes) == 0:
                self.inventory.set_variable(host['name'], "retry_check_interval", host['retry_check_interval'])
            if 'check_timeperiod' in attributes or len(attributes) == 0:
                self.inventory.set_variable(host['name'], "check_timeperiod", host['check_timeperiod'])
            if 'severity' in attributes or len(attributes) == 0:
                self.inventory.set_variable(host['name'], "severity", host['severity'])
            if 'categories' in attributes or len(attributes) == 0:
                self.inventory.set_variable(host['name'], "list_categories", host['categories'])
            self.inventory.set_variable(host['name'], "list_groups", host['groups'])
            if 'is_activated' in attributes or len(attributes) == 0:
                self.inventory.set_variable(host['name'], "is_activated", host['is_activated'])
