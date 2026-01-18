# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: find_all_host_template_configurations
short_description: Return all host template configurations.
description:
    - Return all host template configurations with search options
author: "Pierre ARNOUD (@parnoud)"
options:
    search:
        description: search criteria for fetching host templates (list or dict).
        type: raw
        required: false
        default: null
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Return all host template configurations.
  parnoud.centreon.find_all_host_template_configurations:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass

- name: Return all host template configurations who name start with test
  parnoud.centreon.find_all_host_template_configurations:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        search:
            - "name":
                "$rg": "^test"

- name: Return all host template configurations who name like test or tst
  parnoud.centreon.find_all_host_template_configurations:
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
    description: Return all host template configurations
    returned: success
    type: list
    sample :
        [
            {
                "id": 1,
                "name": "generic-active-host",
                "alias": "generic-active-host",
                "snmp_version": "2c",
                "timezone_id": 1,
                "severity_id": 1,
                "check_command_id": 1,
                "check_command_args": [],
                "check_timeperiod_id": 1,
                "max_check_attempts": 0,
                "normal_check_interval": 0,
                "retry_check_interval": 0,
                "active_check_enabled": 0,
                "passive_check_enabled": 0,
                "notification_enabled": 0,
                "notification_options": 5,
                "notification_interval": 0,
                "notification_timeperiod_id": 1,
                "add_inherited_contact_group": true,
                "add_inherited_contact": true,
                "first_notification_delay": 0,
                "recovery_notification_delay": 0,
                "acknowledgement_timeout": 0,
                "freshness_checked": 0,
                "freshness_threshold": 0,
                "flap_detection_enabled": 0,
                "low_flap_threshold": 0,
                "high_flap_threshold": 0,
                "event_handler_enabled": 0,
                "event_handler_command_id": 1,
                "event_handler_command_args": [],
                "note_url": "string",
                "note": "string",
                "action_url": "string",
                "icon_id": 1,
                "icon_alternative": "string",
                "comment": "string",
                "is_locked": true
            }
        ]
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_template import find_all_host_template_configurations


def find_all_host_template_configurations_with_search(module):
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

    result = find_all_host_template_configurations(api, params=filter_criteria)
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
    status, result = find_all_host_template_configurations_with_search(module)
    if status >= 0:
        module.exit_json(skipped=True, result=result)
    else:
        module.fail_json(result=0)


if __name__ == '__main__':
    main()
