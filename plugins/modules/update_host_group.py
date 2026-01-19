# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: update_host_group
short_description: Update host group.
description:
    - Update host group. with givens parameters
    - API Limitation, We are forced to send a hosts list (empty or not)
    - Default hosts list is empty so if you don't mention it it will wipe hosts associated with the host group
author: "Pierre ARNOUD (@parnoud)"
options:
    hostgroup_id:
        description: Host group ID
        required: true
        type: int
    name:
        description: Host group name
        required: False
        type: str
        default: null
    alias:
        description: Host group alias
        required: False
        type: str
        default: null
    icon_id:
        description: Define the image ID that should be associated with this host group
        required: False
        type: int
        default: null
    geo_coords:
        description: Geographical coordinates use by Centreon Map module to position element on map
        required: False
        type: str
        default: null
    comment:
        description: Comments on this host group
        required: False
        type: str
        default: null
    hosts:
        description: Hosts linked to this host group
        required: False
        type: list
        elements: int
        default: []
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Create host group configuration
  parnoud.centreon.add_host_group:
    hostname: centreon.com/centreon/api/latest
    username: user
    password: pass
    name: my-host-group
'''

RETURN = r'''
---
result:
    description: Update host group configuration
    returned: success
    type: dict
    sample :
        {
            "name": "MySQL-Servers",
            "alias": "All MySQL Servers",
            "icon": {
                "id": 1,
                "name": "folder/image.png",
                "url": "/centreon/img/media/folder/image.png"
            },
            "geo_coords": "48.51,2.20",
            "comment": "string",
            "hosts": [
                {
                    "id": 1,
                    "name": "HostName-01"
                }
            ]
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_group import add_host_group


def add_host_group_with_parameters(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )
    hostgroup_data = {
        'name': module.params.get('name'),
        'alias': module.params.get('alias'),
        'icon_id': module.params.get('icon_id'),
        'geo_coords': module.params.get('geo_coords'),
        'comment': module.params.get('comment'),
        'hosts': module.params.get('hosts'),
    }

    hostgroup_data = {k: v for k, v in hostgroup_data.items() if v is not None}

    result = add_host_group(api, hostgroup_id=module.params.get('hostgroup_id'), hostgroup_data=hostgroup_data)
    return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        hostgroup_id=dict(type='int', required=True),
        name=dict(type='str', default=None),
        alias=dict(type='str', default=None),
        icon_id=dict(type='int', default=None),
        geo_coords=dict(type='str', default=None),
        comment=dict(type='str', default=None),
        hosts=dict(type='list', elements='int', default=[]),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = add_host_group_with_parameters(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result=[])


if __name__ == '__main__':
    main()
