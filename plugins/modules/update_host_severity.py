# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: update_host_severity
short_description: Update a host severity
description:
    - Update host group sevirity with givens parameters
author: "Pierre ARNOUD (@parnoud)"
options:
    hostseverity_id:
        description: ID of existing host severity configuration
        required: True
        type: int
    name:
        description: Host severity name
        required: True
        type: str
        default: null
    alias:
        description: Host severity alias
        type: str
        default: null
        required: True
    level:
        description: Host severity priority
        type: int
        default: null
        required: True
    icon_id:
        description: Define the image ID associated with this severity
        type: int
        default: null
        required: True
    comment:
        description: Host severity comment.
        type: str
        default: null
        required: False
    is_activated:
        description: Indicates whether this host severity is enabled or not
        type: bool
        default: true
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Update host sevirity configuration
  parnoud.centreon.update_host_severity:
    hostname: centreon.com/centreon/api/latest
    username: user
    password: pass
    name: my-host-severity
    alias: my-host-severity
    level: 1
    icon_id: 1
    comment: test-severity
'''

RETURN = r'''
---
result:
    description: Update host sevirity configuration
    returned: success
    type: dict
    sample :
        {
            "name": "host-severity",
            "alias": "host-severity",
            "level": 2,
            "icon_id": 1,
            "comment": "string",
            "is_activated": true
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_severity import update_host_severity


def update_host_severity_with_parameters(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )
    hostseverity_data = {
        'name': module.params.get('name'),
        'alias': module.params.get('alias'),
        'level': module.params.get('level'),
        'icon_id': module.params.get('icon_id'),
        'comment': module.params.get('comment'),
        'is_activated': module.params.get('is_activated'),
    }

    hostseverity_data = {k: v for k, v in hostseverity_data.items() if v is not None}

    result = update_host_severity(api, hostseverity_id=module.params.get('hostseverity_id'), hostseverity_data=hostseverity_data)
    return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        hostseverity_id=dict(type='int', required=True),
        name=dict(type='str', required=True),
        alias=dict(type='str', required=True),
        level=dict(type='int', required=True),
        icon_id=dict(type='int', required=True),
        comment=dict(type='str', default=None),
        is_activated=dict(type='bool', default=True),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = update_host_severity_with_parameters(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(object=[])


if __name__ == '__main__':
    main()
