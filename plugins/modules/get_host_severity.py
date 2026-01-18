# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: get_host_severity
short_description: Get a host severity configuration
description:
    - Get a host severity configuration with the given host_id
author: "Pierre ARNOUD (@parnoud)"
options:
    hostseverity_id:
        description: hostseverity id
        required: True
        type: int
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Get a host severity configuration
  parnoud.centreon.get_host_severity:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        hostseverity_id: 5
'''

RETURN = r'''
---
result:
    description: dict of host sevirity configuration
    returned: success
    type: dict
    sample :
        {
            "id": 1,
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
from ansible_collections.parnoud.centreon.plugins.module_utils.host_severity import get_host_severity


def get_host_severity_by_id(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )

    result = get_host_severity(api, hostseverity_id=module.params.get('hostseverity_id'))
    return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        hostseverity_id=dict(type='int', required=True),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = get_host_severity_by_id(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result={})


if __name__ == '__main__':
    main()
