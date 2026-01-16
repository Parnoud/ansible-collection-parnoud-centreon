# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: manage_host_groups
short_description: Create a host in Centreon via API v2
description:
    - Create a host group in Centreon.
    - Update a host group in Centreon.
    - Delete a host group in Centreon.
author: "Pierre ARNOUD (@parnoud)"
options:
    state:
        description: Desired state of the host.
        choices: ['create', 'delete', 'update', 'duplicate']
        default: 'create'
        type: str
        required: False
    name:
        description: Name of the host group.
        required: False
        type: str
    new_name:
        description: New name of the host (for update state).
        required: False
        type: str
    alias:
        description: Alias of the host.
        required: False
        type: str
    icon_id:
        description: Icon ID of the host.
        required: False
        type: int
    geo_coords:
        description: Geographical coordinates of the host.
        required: False
        type: str
    comment:
        description: Comment for the host.
        required: False
        type: str
    hosts:
        description: Dictionary of hosts to be associated with the host group.
        required: False
        type: list
        elements: int
        default: []
    ids:
        description: Dictionary of hosts ids to duplicate.
        required: False
        type: list
        elements: int
    nb_duplicates:
        description: Number of duplicates to create.
        required: False
        type: int
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''

'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.host_group import (
    delete_host_group,
    update_host_group,
    list_all_host_groups,
    add_host_group,
    duplicate_multiple_host_groups,
    get_host_groups
)
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec


def manage_host_groups(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
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
        return True, result

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
                return False, f"Host group {module.params['name']} multiple or not found for update."
            host_group_id = hosts[0]['id']

        if host_group_id:
            if update_host_group(api, host_group_id, host_group_data):
                return True, get_host_groups(api, host_group_id)
        else:
            return False, "Host ID or name must be provided for update operation."

    elif module.params['state'] == 'delete':

        host_group_id = None

        if module.params['host_id']:
            host_group_id = module.params['host_id']
        elif module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})
            host_groups = list_all_host_groups(api, query_parameters=filter_criteria)

            if len(host_groups) == 0:
                return True, host_groups
            elif len(host_groups) >= 2:
                return False, f"Host {module.params['name']} multiple for update. {len(host_groups)}"
            host_group_id = host_groups[0]['id']

        if host_group_id:
            if delete_host_group(api, host_group_id):
                return True, host_groups[0]
        else:
            return False, "Host ID or name must be provided for update operation."

    elif module.params['state'] == 'duplicate':
        result = duplicate_multiple_host_groups(api, module.params.get('ids'), module.params.get('nb_duplicates'))
        return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        state=dict(type='str', choices=['create', 'delete', 'update', 'duplicate'], default='create'),
        name=dict(type='str'),
        new_name=dict(type='str'),
        alias=dict(type='str'),
        icon_id=dict(type='int', default=None),
        geo_coords=dict(type='str', default=None),
        comment=dict(type='str', default=None),
        hosts=dict(type='list', elements='int', default=[]),
        ids=dict(type='list', elements='int'),
        nb_duplicates=dict(type='int')
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    return_type, data = manage_host_groups(module)
    if return_type:
        module.exit_json(changed=False, data=data)
    else:
        module.fail_json(msg=data)


if __name__ == '__main__':
    main()
