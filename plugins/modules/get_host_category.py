# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: get_host_category
short_description: Get a host category configuration
description:
    - Get a host category configuration with the given host_id
author: "Pierre ARNOUD (@parnoud)"
options:
    hostcategory_id:
        description: ID of existing host category configuration
        required: True
        type: int
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Get a host category configuration
  parnoud.centreon.get_host_category:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        hostcategory_id: 5
'''

RETURN = r'''
---
result:
    description: dict of host category configuration
    returned: success
    type: dict
    sample :
        {
            "id": 1,
            "name": "host-category",
            "alias": "host-category",
            "is_activated": true,
            "comment": "string"
        }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_category import get_host_category


def get_host_category_by_id(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )

    result = get_host_category(api, hostcategory_id=module.params.get('hostcategory_id'))
    return True, result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        hostcategory_id=dict(type='int', required=True),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = get_host_category_by_id(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result={})


if __name__ == '__main__':
    main()
