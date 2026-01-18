# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: reload_configuration_monitoring_server
short_description: Reload the configuration files of the monitoring server
description:
    - Reload the configuration files of the monitoring server by id
author: "Pierre ARNOUD (@parnoud)"
options:
    monitoring_server_id:
        description: ID of the monitoring server (poller)
        required: true
        type: int
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Generate and move the configuration files of the monitoring server
  parnoud.centreon.reload_configuration_monitoring_server:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        monitoring_server_id: 1
'''

RETURN = r'''
---
result:
    description: Reload the configuration files of the monitoring server
    returned: success
    type: str
    sample : OK
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.monitoring_server import reload_configuration_monitoring_server


def reload_configuration_monitoring_server_by_id(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )

    if reload_configuration_monitoring_server(api, monitoring_server_id=module.params.get('monitoring_server_id')):
        return True, 'OK'
    else:
        return False, 'NOK'


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        monitoring_server_id=dict(type='int', required=True),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, result = reload_configuration_monitoring_server_by_id(module)
    if status:
        module.exit_json(succes=True, result=result)
    else:
        module.fail_json(result=result)


if __name__ == '__main__':
    main()
