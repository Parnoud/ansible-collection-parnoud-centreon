# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: list_all_host_categories
short_description: List of host category configurations
description:
    - Return all host group configurations with search options
author: "Pierre ARNOUD (@parnoud)"
options:
    search:
        description: Retrieve only data matching the defined search value.
        type: raw
        required: false
        default: null
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: List of host category configurations
  parnoud.centreon.list_all_host_categories:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass

- name: List of host category configurations who start with test
  parnoud.centreon.list_all_host_categories:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        search:
            - "name":
                "$rg": "^test"

- name: List of host category configurations who name like test or tst
  parnoud.centreon.list_all_host_categories:
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
---
result:
    description: List of host category configurations
    returned: success
    type: list
    sample :
        [
            {
                "id": 1,
                "name": "host-category",
                "alias": "host-category",
                "is_activated": true,
                "comment": "string"
            }
        ]
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_category import list_host_caterogies


def list_host_categories_with_search(module):
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

    result = list_host_caterogies(api, params=filter_criteria)
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
    status, result = list_host_categories_with_search(module)
    if status >= 0:
        module.exit_json(skipped=True, result=result)
    else:
        module.fail_json(result=0)


if __name__ == '__main__':
    main()
