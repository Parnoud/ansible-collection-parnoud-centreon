# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: create_host_severity
short_description: Create a host configuration
description:
    - Create host configuration with givens parameters
author: "Pierre ARNOUD (@parnoud)"
options:
    name:
        description: Host severity name.
        required: True
        type: str
    alias:
        description: Host severity alias.
        required: True
        type: str
    level:
        description: Host severity level.
        required: True
        type: int
    icon_id:
        description: Host severity icon id.
        required: True
        type: int
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Create a host severity
  parnoud.centreon.create_host_severity:
    hostname: centreon.com/centreon/api/latest
    username: user
    password: pass
    name: test-severity
    alias: test-severity
    level: 1
    icon_id: 1

'''

RETURN = r'''
---
result:
    description: Empty to indicate succes
    returned: success
    type: dict
    sample :
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_severity import create_host_severity


def create_host_severity_with_parameters(module):
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
    }

    hostseverity_data = {k: v for k, v in hostseverity_data.items() if v is not None}

    result = create_host_severity(api, hostseverity_data=hostseverity_data)
    return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        alias=dict(type='str', required=True),
        level=dict(type='int', required=True),
        icon_id=dict(type='int', required=True),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = create_host_severity_with_parameters(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result=[])


if __name__ == '__main__':
    main()
