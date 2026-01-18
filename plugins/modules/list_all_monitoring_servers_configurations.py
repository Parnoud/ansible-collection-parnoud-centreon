# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: list_all_monitoring_servers_configurations
short_description: List all monitoring servers configurations.
description:
    - List all monitoring servers configurations with search options
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
- name: Search all monitoring servers
  parnoud.centreon.list_all_monitoring_servers_configurations:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass

- name: Search all monitoring servers name who start with test
  parnoud.centreon.list_all_monitoring_servers_configurations:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        search:
            - "name":
                "$rg": "^test"

- name: Search all monitoring servers who name like test or tst
  parnoud.centreon.list_all_monitoring_servers_configurations:
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
    description: List all monitoring servers configurations
    returned: success
    type: list
    sample :
        [
            {
                "id": 2,
                "name": "Central",
                "address": "127.0.0.1",
                "is_localhost": true,
                "is_default": true,
                "ssh_port": 22,
                "last_restart": "2019-08-24T14:15:22Z",
                "engine_start_command": "service centengine start",
                "engine_stop_command": "service centengine stop",
                "engine_restart_command": "service centengine restart",
                "engine_reload_command": "service centengine reload",
                "nagios_bin": "/usr/sbin/centengine",
                "nagiostats_bin": "/usr/sbin/centenginestats",
                "broker_reload_command": "service cbd reload",
                "centreonbroker_cfg_path": "/etc/centreon-broker",
                "centreonbroker_module_path": "/usr/share/centreon/lib/centreon-broker",
                "centreonbroker_logs_path": null,
                "centreonconnector_path": "/usr/lib64/centreon-connector",
                "init_script_centreontrapd": "centreontrapd",
                "snmp_trapd_path_conf": "/etc/snmp/centreon_traps/",
                "remote_id": null,
                "remote_server_use_as_proxy": true,
                "is_updated": true,
                "is_activate": true
            }
        ]
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.monitoring_server import list_all_monitoring_server_configurations


def list_all_monitoring_server_configurations_with_search(module):
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

    result = list_all_monitoring_server_configurations(api, params=filter_criteria)
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
    status, result = list_all_monitoring_server_configurations_with_search(module)
    if status >= 0:
        module.exit_json(skipped=True, result=result)
    else:
        module.fail_json(result=0)


if __name__ == '__main__':
    main()
