# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: create_host_category
short_description: Create a host category
description:
    - Create host configuration with givens parameters
author: "Pierre ARNOUD (@parnoud)"
options:
    name:
        description: Host category name
        required: True
        type: str
    alias:
        description: Host category alias
        required: True
        type: str
    is_activated:
        description: is active or not (enable/disable)
        type: bool
        default: True
    comment:
        description: some comment
        required: False
        type: str
        default: null
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Create a host category
  parnoud.centreon.create_host_category:
    hostname: centreon.com/centreon/api/latest
    username: user
    password: pass
    name: host-category
    alias: host-category
'''

RETURN = r'''
---
result:
    description: dict with created datas
    returned: success
    type: dict
    sample :
        {
            "name": "host-category",
            "alias": "host-category",
            "is_activated": true,
            "comment": ""
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_category import create_host_category


def create_host_category_with_parameters(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )
    hostcategory_data = {
        'name': module.params.get('name'),
        'alias': module.params.get('alias'),
        'is_activated': module.params.get('is_activated'),
        'comment': module.params.get('comment'),
    }

    hostcategory_data = {k: v for k, v in hostcategory_data.items() if v is not None}

    result = create_host_category(api, hostcategory_data=hostcategory_data)
    return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        alias=dict(type='str', required=True),
        is_activated=dict(type='bool', default=True),
        comment=dict(type='str', default=None),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = create_host_category_with_parameters(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result=[])


if __name__ == '__main__':
    main()
