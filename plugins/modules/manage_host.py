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
    - Create a host in Centreon.
author: "Pierre ARNOUD (@parnoud)"
options:
    state:
        description: Desired state of the host.
        choices: ['present', 'absent', 'update']
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
    monitoring_server_id:
        description: ID of the monitoring server where the host will be created.
        required: false
        type: int
    host_id:
        description: Host id.
        required: false
        type: int
    name:
        description: Host name.
        required: false
        type: str
    new_name:
        description: New host name for update operation.
        required: false
        type: str
    address:
        description: Host address.
        required: false
        type: str
'''

EXAMPLES = r'''

'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.host import delete_host_configuration, partially_update_host_configuration, find_all_host_configuration, create_host_configuration
import json


def main():
    """entry point for module execution"""

    spec = {
        'state': {
            'type': 'str',
            'default': 'create',
            'choices': ['create', 'delete', 'update'],
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
        'monitoring_server_id': {
            'type': 'int',
            'required': False,
        },
        'host_id': {
            'type': 'int',
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
        'address': {
            'type': 'str',
            'required': False,
        }
    }

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_one_of=[['token', 'username', 'password']],
        mutually_exclusive=[['token', 'username'], ['token', 'password']],
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

    if module.params['state'] == 'create':
        host_data={
            'monitoring_server_id': module.params['monitoring_server_id'],
            'name': module.params['name'],
            'address': module.params['address'],
        }
        result = create_host_configuration(api, host_data=host_data)
        module.exit_json(Created=True, result=result['id'])
        
    elif module.params['state'] == 'update':
        host_data={
            'address': module.params['address'],
        }

        host_id = None

        if module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})
            hosts = find_all_host_configuration(api, query_parameters=filter_criteria)
            if len(hosts) != 1:
                module.fail_json(msg=f"Host {module.params['name']} multiple or not found for update.")
            host_id = hosts[0]['id']
        elif module.params['host_id']:
            host_id = module.params['host_id']

        if partially_update_host_configuration(api, host_id, host_data):
            module.exit_json(changed=True, result={"host_id": host_id, "status": "updated"})

    elif module.params['state'] == 'delete':
        host_id = None

        if module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})

            hosts = find_all_host_configuration(api, query_parameters=filter_criteria)
            if len(hosts) != 1:
                module.fail_json(msg=f"Host {module.params['name']} multiple or not found for update. {len(hosts)}")
            host_id = hosts[0]['id']
        elif module.params['host_id']:
            host_id = module.params['host_id']

        if delete_host_configuration(api, host_id):
            module.exit_json(changed=True, result={"host_id": host_id, "status": "deleted"})

if __name__ == '__main__':
    main()
