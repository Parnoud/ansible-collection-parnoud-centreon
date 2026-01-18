# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: delete_host_severity
short_description: Delete a host severity configuration
description:
    - Delete a host severity configurationwith the given hostseverity_id
author: "Pierre ARNOUD (@parnoud)"
options:
    hostseverity_id:
        description: ID of existing host severity configuration
        required: True
        type: int
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Delete host group by id
  parnoud.centreon.delete_host_severity:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        hostseverity_id: 32
'''

RETURN = r'''
---
hostseverity_id:
    description: 0 to indicate delete
    returned: success
    type: int
    sample : 0
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host_severity import delete_host_severity


def delete_host_severity_by_id(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )

    if delete_host_severity(api, hostseverity_id=module.params.get('hostseverity_id')):
        return True, 0
    else:
        return False, module.params.get('hostseverity_id')


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        hostseverity_id=dict(type='int', required=True),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, hostseverity_id = delete_host_severity_by_id(module)
    if status:
        module.exit_json(succes=True, hostseverity_id=hostseverity_id)
    else:
        module.fail_json(hostseverity_id=hostseverity_id)


if __name__ == '__main__':
    main()
