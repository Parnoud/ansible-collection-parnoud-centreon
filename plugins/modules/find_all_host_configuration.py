# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: find_all_host_configuration
short_description: Find all host configuration
description:
    - Find all host configuration with search options
author: "Pierre ARNOUD (@parnoud)"
options:
    search:
        description: search criteria for fetching hosts (list or dict).
        type: raw
        required: false
        default: none
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
- name: Search all host
    parnoud.centreon.find_all_host_configuration:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass

- name: Search all host who start with test
    parnoud.centreon.find_all_host_configuration:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        search:
            - "name":
                "$rg": "^test"

- name: Search all host who name like test or tst
    parnoud.centreon.find_all_host_configuration:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        search:
          "$or":
            - "name":
                "$rg": "^serveur"
            - "name":
                "$rg": "^my"
'''

RETURN = r'''
host_id:
    description: 0 to indicate delete
    returned: success
    type: int
    sample : 0
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host import find_all_host_configuration


def find_all_host_configuration_with_search(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )
    search_criteria = module.params.get('search') or None
    filter_criteria = None
    if search_criteria:
        filter_criteria = {}
        filter_criteria['search'] = json.dumps(search_criteria)

    result = find_all_host_configuration(api, params=filter_criteria)
    return len(result), result


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        search=dict(type='raw', default=None),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = find_all_host_configuration_with_search(module)
    if status == 0:
        module.exit_json(skipped=True, result=result)
    elif status >= 1:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result=0)


if __name__ == '__main__':
    main()
