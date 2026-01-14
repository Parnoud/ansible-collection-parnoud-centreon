# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: manage_host
short_description: Create a host in Centreon via API v2
description:
    - Create a host group in Centreon.
    - Update a host group in Centreon.
    - Delete a host group in Centreon.
author: "Pierre ARNOUD (@parnoud)"
state:
        description: Desired state of the host.
        choices: ['present', 'absent', 'update', 'duplicate']
        default: 'present'
        type: str
    hostname:
        description: URL to Centreon API v2.
        required: false
        type: str
    port:
        description: Port to Centreon API v2.
        required: false
        type: int
    token:
        description: Centreon API token.
        required: false
        type: str
    username:
        description: Centreon username.
        required: false
        type: str
    password:
        description: Centreon password.
        required: false
        type: str
    validate_certs:
        description: Whether to validate SSL certificates.
        type: bool
        default: false
        required: false
    timeout:
        description: Timeout for API requests.
        type: int
        default: 30
        required: false
    name:
        description: Name of the host group.
        required: false
        type: str
    new_name:
        description: New name of the host (for update state).
        required: false
        type: str
    alias:
        description: Alias of the host.
        required: false
        type: str
    icon_id:
        description: Icon ID of the host.
        required: false
        type: int
    geo_coords:
        description: Geographical coordinates of the host.
        required: false
        type: str
    comment:
        description: Comment for the host.
        required: false
        type: str
    hosts:
        description: Dictionary of hosts to be associated with the host group.
        required: false
        type: list
        default: []
    ids:
        description: Dictionary of hosts ids to duplicate.
        required: false
        type: list
    nb_duplicates:
        description: Number of duplicates to create.
        required: false
        type: int
'''

EXAMPLES = r'''

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.host_group import delete_host_group, update_host_group, list_all_host_groups, add_host_group, duplicate_multiple_host_groups
import json

def main():
    """entry point for module execution"""

    spec = {
        'state': {
            'type': 'str',
            'default': 'create',
            'choices': ['create', 'delete', 'update', 'duplicate'],
        },
        'hostname': {
            'type': 'str',
            'required': False,
        },
        'port': {
            'type': 'int',
            'required': False,
        },
        'token': {
            'type': 'str',
            'required': False,
            'no_log': True,
        },
        'username': {
            'type': 'str',
            'required': False,
        },
        'password': {
            'type': 'str',
            'required': False,
            'no_log': True,
        },
        'validate_certs': {
            'type': 'bool',
            'default': False,
            'required': False,
        },
        'timeout': {
            'type': 'int',
            'default': 30,
            'required': False,
        },
        'name': {
            'type': 'str',
            'required': False,
        },
        'new_name': {
            'type': 'str',
            'required': False,
        },
        'alias': {
            'type': 'str',
            'required': False,
            'default': None,
        },
        'icon_id': {
            'type': 'int',
            'required': False,
            'default': None,
        },
        'geo_coords': {
            'type': 'str',
            'required': False,
            'default': None,
        },
        'comment': {
            'type': 'str',
            'required': False,
            'default': None,
        },
        'hosts': {
            'type': 'list',
            'required': False,
            'default': [],
        },
        'ids': {
            'type': 'list',
            'required': False,
        },
        'nb_duplicates' : {
            'type': 'int',
            'required': False,
        },

    }

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_one_of=[['token', 'username', 'password', 'name', 'host_id']],
        mutually_exclusive=[['token', 'username'], ['token', 'password'], ['name', 'host_id']],
    )

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        port=module.params.get('port'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )

    host_group_data = {
        'alias': module.params.get('alias'),
        'comment': module.params.get('comment'),
        'geo_coords': module.params.get('geo_coords'),
        'hosts': module.params.get('hosts'),
        'icon_id': module.params.get('icon_id'),
        'name': module.params.get('name'),
    }

    host_group_data = {k: v for k, v in host_group_data.items() if v is not None}

    if module.params['state'] == 'create':

        result = add_host_group(api, host_group_data=host_group_data)
        module.exit_json(Created=True, result=result['name'])

    elif module.params['state'] == 'update':

        host_group_id = None
        if module.params['new_name']:
            host_group_data['name'] = module.params['new_name']
        else:
            host_group_data.pop('name', None)
        
        if module.params['host_id']:
            host_group_id = module.params['host_id']
        elif module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})
            hosts = list_all_host_groups(api, params=filter_criteria)
            if len(hosts) != 1:
                module.fail_json(msg=f"Host group {module.params['name']} multiple or not found for update.")
            host_group_id = hosts[0]['id']
        

        if host_group_id:
            if update_host_group(api, host_group_id, host_group_data):
                module.exit_json(changed=True, result={"host_id": host_group_id, "status": "updated"})
        else:
            module.fail_json(msg="Host ID or name must be provided for update operation.")
    
    elif module.params['state'] == 'delete':

        host_group_id = None
        
        if module.params['host_id']:
            host_group_id = module.params['host_id']
        elif module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})
            hosts = list_all_host_groups(api, query_parameters=filter_criteria)
            if len(hosts) != 1:
                module.fail_json(msg=f"Host group {module.params['name']} multiple or not found for update.")
            host_group_id = hosts[0]['id']
        

        if host_group_id:
            if delete_host_group(api, host_group_id):
                module.exit_json(changed=True, result={"host_id": host_group_id, "status": "updated"})
        else:
            module.fail_json(msg="Host ID or name must be provided for update operation.")

    elif module.params['state'] == 'duplicate':
        result=duplicate_multiple_host_groups(api, module.params.get('ids'), module.params.get('nb_duplicates'))
if __name__ == '__main__':
    main()
