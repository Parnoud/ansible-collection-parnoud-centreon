# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: update_host_category
short_description: Update a host severity
description:
    - Update host group sevirity with givens parameters
author: "Pierre ARNOUD (@parnoud)"
options:
    hostcategory_id:
        description: ID of existing host category configuration
        required: True
        type: int
    name:
        description: Host category name
        type: str
        default: null
    alias:
        description: Host category alias
        type: str
        default: null
    is_activated:
        description: is active or not (enable/disable)
        type: bool
        default: null
    comment:
        description: some comment
        type: str
        default: null
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Update a host category
  parnoud.centreon.update_host_category:
    hostname: centreon.com/centreon/api/latest
    username: user
    password: pass
    name: my-host-severity
    alias: my-host-severity
    is_activated: True
    comment: 1
'''

RETURN = r'''
---
result:
    description: dict of host category
    returned: success
    type: dict
    sample :
        {
            "name": "host-category",
            "alias": "host-category",
            "is_activated": true,
            "comment": "string"
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_category import update_host_category


def update_host_category_with_parameters(module):
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

    result = update_host_category(api, hostcategory_id=module.params.get('hostcategory_id'), hostcategory_data=hostcategory_data)
    return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        hostcategory_id=dict(type='int', required=True),
        name=dict(type='str', default=None),
        alias=dict(type='str', default=None),
        is_activated=dict(type='bool', default=None),
        comment=dict(type='str', default=None),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = update_host_category_with_parameters(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result=[])


if __name__ == '__main__':
    main()
