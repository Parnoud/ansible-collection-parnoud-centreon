# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: manage_host
short_description: Create a host in Centreon via API v2
description:
    - Create a host in Centreon.
author: "Pierre ARNOUD (@parnoud)"
options:
    state:
        description: Desired state of the host.
        choices: ['present', 'absent', 'update']
        default: 'present'
        type: str
    hostname:
        description: URL to Centreon API v2.
        required: false
        type: str
    port:
        description: Port to Centreon API v2.
        required: false
        type: int
    token:
        description: Centreon API token.
        required: false
        type: str
    username:
        description: Centreon username.
        required: false
        type: str
    password:
        description: Centreon password.
        required: false
        type: str
    validate_certs:
        description: Whether to validate SSL certificates.
        type: bool
        default: false
        required: false
    timeout:
        description: Timeout for API requests.
        type: int
        default: 30
        required: false
    monitoring_server_id:
        description: ID of the monitoring server where the host will be created.
        required: false
        type: int
    host_id:
        description: Host id.
        required: false
        type: int
    name:
        description: Host name.
        required: false
        type: str
    new_name:
        description: New host name for update operation.
        required: false
        type: str
    address:
        description: Host address.
        required: false
        type: str
    alias:
        description: Host alias.
        required: false
        type: str
    snmp_community:
        description: SNMP community string.
        required: false
        type: str
    snmp_version:
        description: SNMP version.
        required: false
        type: str
        choices: ['1', '2c', '3']
    geo_coords:
        description: Geographical coordinates of the host.
        required: false
        type: str
    timezone_id:
        description: Timezone ID for the host.
        required: false
        type: int
    severity_id:
        description: Severity ID for the host.
        required: false
        type: int
    check_command_id:
        description: Check command ID for the host.
        required: false
        type: int
    check_command_args:
        description: Arguments for the check command.
        required: false
        type: dict
    check_timeperiod_id:
        description: Check time period ID for the host.
        required: false
        type: int
    max_check_attempts:
        description: Maximum number of check attempts.
        required: false
        type: int
    normal_check_interval:
        description: Normal check interval.
        required: false
        type: int
    retry_check_interval:
        description: Retry check interval.
        required: false
        type: int
    active_check_enabled:
        description: Whether active checks are enabled.
        required: false
        type: int
        choices: [0, 1, 2]
    passive_check_enabled:
        description: Whether passive checks are enabled.
        required: false
        type: int
        choices: [0, 1, 2]
    notifications_enabled:
        description: Whether notifications are enabled.
        required: false
        type: int
        choices: [0, 1, 2]
    notification_options:
        description: Notification options.
        required: false
        type: int
        choices: [0, 1, 2, 4, 8, 16]
    notification_interval:
        description: Notification interval.
        required: false
        type: int
    notification_timeperiod_id:
        description: Notification time period ID.
        required: false
        type: int
    add_inherited_contact_group:
        description: Whether to add inherited contact groups.
        required: false
        type: bool
    add_inherited_contact:
        description: Whether to add inherited contacts.
        required: false
        type: bool
    first_notification_delay:
        description: First notification delay.
        required: false
        type: int
    recovery_notification_delay:
        description: Recovery notification delay.
        required: false
        type: int
    acknowledgement_timeout:
        description: Acknowledgement timeout.
        required: false
        type: int
    freshness_threshold:
        description: Freshness threshold.
        required: false
        type: int
    flap_detection_enabled:
        description: Whether flap detection is enabled.
        required: false
        type: int
        choices: [0, 1, 2]
    low_flap_threshold:
        description: Low flap threshold.
        required: false
        type: int
    high_flap_threshold:
        description: High flap threshold.
        required: false
        type: int
    event_handler_enabled:
        description: Whether event handler is enabled.
        required: false
        type: int
        choices: [0, 1, 2]
    event_handler_command_id:
        description: Event handler command ID.
        required: false
        type: int
    event_handler_command_args:
        description: Arguments for the event handler command.
        required: false
        type: dict
    note_url:
        description: Note URL for the host.
        required: false
        type: str
    note:
        description: Note for the host.
        required: false
        type: str
    action_url:
        description: Action URL for the host.
        required: false
        type: str
    icon_id:
        description: Icon ID for the host.
        required: false
        type: int
    icon_alternative:
        description: Icon alternative text for the host.
        required: false
        type: str
    comment:
        description: Comment for the host.
        required: false
        type: str
    is_activated:
        description: Whether the host is activated.
        required: false
        type: bool
    categories:
        description: Categories associated with the host.
        required: false
        type: dict
    groups:
        description: Groups associated with the host.
        required: false
        type: dict
    templates:
        description: Templates associated with the host.
        required: false
        type: dict
    macros:
        description: Macros associated with the host.
        required: false
        type: dict
'''

EXAMPLES = r'''

'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.host import delete_host_configuration, partially_update_host_configuration, find_all_host_configuration, create_host_configuration
import json


def main():
    """entry point for module execution"""

    spec = {
        'state': {
            'type': 'str',
            'default': 'create',
            'choices': ['create', 'delete', 'update'],
        },
        'hostname': {
            'type': 'str',
            'required': False,
        },
        'port': {
            'type': 'int',
            'required': False,
        },
        'token': {
            'type': 'str',
            'required': False,
            'no_log': True,
        },
        'username': {
            'type': 'str',
            'required': False,
        },
        'password': {
            'type': 'str',
            'required': False,
            'no_log': True,
        },
        'validate_certs': {
            'type': 'bool',
            'default': False,
            'required': False,
        },
        'timeout': {
            'type': 'int',
            'default': 30,
            'required': False,
        },
        'monitoring_server_id': {
            'type': 'int',
            'required': False,
        },
        'host_id': {
            'type': 'int',
            'required': False,
        },
        'name': {
            'type': 'str',
            'required': False,
        },
        'new_name': {
            'type': 'str',
            'required': False,
        },
        'address': {
            'type': 'str',
            'required': False,
        },
        'alias': {
            'type': 'str',
            'required': False,
        },
        'snmp_community': {
            'type': 'str',
            'required': False,
        },
        'snmp_version': {
            'type': 'str',
            'required': False,
            'choices': ['1', '2c', '3'],
        },
        'geo_coords': {
            'type': 'str',
            'required': False,
        },
        'timezone_id': {
            'type': 'int',
            'required': False,
        },
        'severity_id': {
            'type': 'int',
            'required': False,
        },
        'check_command_id': {
            'type': 'int',
            'required': False,
        },
        'check_command_args': {
            'type': 'dict',
            'required': False,
        },
        'check_timeperiod_id': {
            'type': 'int',
            'required': False,
        },
        'max_check_attempts': {
            'type': 'int',
            'required': False,
        },
        'normal_check_interval': {
            'type': 'int',
            'required': False,
        },
        'retry_check_interval': {
            'type': 'int',
            'required': False,
        },
        'active_check_enabled': {
            'type': 'int',
            'required': False,
            'choices': [0, 1, 2],
        },
        'passive_check_enabled': {
            'type': 'int',
            'required': False,
            'choices': [0, 1, 2],
        },
        'notifications_enabled': {
            'type': 'int',
            'required': False,
            'choices': [0, 1, 2],
        },
        'notification_options': {
            'type': 'int',
            'required': False,
            'choices': [0, 1, 2, 4, 8, 16],
        },
        'notification_interval': {
            'type': 'int',
            'required': False,
        },
        'notification_timeperiod_id': {
            'type': 'int',
            'required': False,
        },
        'add_inherited_contact_group': {
            'type': 'bool',
            'required': False,
        },
        'add_inherited_contact': {
            'type': 'bool',
            'required': False,
        },
        'first_notification_delay': {
            'type': 'int',
            'required': False,
        },
        'recovery_notification_delay': {
            'type': 'int',
            'required': False,
        },
        'acknowledgement_timeout': {
            'type': 'int',
            'required': False,
        },
        'freshness_threshold': {
            'type': 'int',
            'required': False,
        },
        'flap_detection_enabled': {
            'type': 'int',
            'required': False,
            'choices': [0, 1, 2],
        },
        'low_flap_threshold': {
            'type': 'int',
            'required': False,
        },
        'high_flap_threshold': {
            'type': 'int',
            'required': False,
        },
        'event_handler_enabled': {
            'type': 'int',
            'required': False,
            'choices': [0, 1, 2],
        },
        'event_handler_command_id': {
            'type': 'int',
            'required': False,
        },
        'event_handler_command_args': {
            'type': 'dict',
            'required': False,
        },
        'note_url': {
            'type': 'str',
            'required': False,
        },
        'note': {
            'type': 'str',
            'required': False,
        },
        'action_url': {
            'type': 'str',
            'required': False,
        },
        'icon_id': {
            'type': 'int',
            'required': False,
        },
        'icon_alternative': {
            'type': 'str',
            'required': False,
        },
        'comment': {
            'type': 'str',
            'required': False,
        },
        'is_activated': {
            'type': 'bool',
            'required': False,
        },
        'categories': {
            'type': 'dict',
            'required': False,
        },
        'groups': {
            'type': 'dict',
            'required': False,
        },
        'templates': {
            'type': 'dict',
            'required': False,
        },
        'macros': {
            'type': 'dict',
            'required': False,
        },
    }

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        required_one_of=[['token', 'username', 'password', 'name', 'host_id']],
        mutually_exclusive=[['token', 'username'], ['token', 'password'], ['name', 'host_id']],
    )

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
        port=module.params.get('port'),
        token=module.params.get('token'),
        username=module.params.get('username'),
        password=module.params.get('password'),
        validate_certs=module.params.get('validate_certs'),
        timeout=module.params.get('timeout'),
    )

    host_data = {
        'monitoring_server_id': module.params.get('monitoring_server_id'),
        'name': module.params.get('name'),
        'address': module.params.get('address'),
        'alias': module.params.get('alias'),
        'snmp_community': module.params.get('snmp_community'),
        'snmp_version': module.params.get('snmp_version'),
        'geo_coords': module.params.get('geo_coords'),
        'timezone_id': module.params.get('timezone_id'),
        'severity_id': module.params.get('severity_id'),
        'check_command_id': module.params.get('check_command_id'),
        'check_command_args': module.params.get('check_command_args'),
        'check_timeperiod_id': module.params.get('check_timeperiod_id'),
        'max_check_attempts': module.params.get('max_check_attempts'),
        'normal_check_interval': module.params.get('normal_check_interval'),
        'retry_check_interval': module.params.get('retry_check_interval'),
        'active_check_enabled': module.params.get('active_check_enabled'),
        'passive_check_enabled': module.params.get('passive_check_enabled'),
        'notifications_enabled': module.params.get('notifications_enabled'),
        'notification_options': module.params.get('notification_options'),
        'notification_interval': module.params.get('notification_interval'),
        'notification_timeperiod_id': module.params.get('notification_timeperiod_id'),
        'add_inherited_contact_group': module.params.get('add_inherited_contact_group'),
        'add_inherited_contact': module.params.get('add_inherited_contact'),
        'first_notification_delay': module.params.get('first_notification_delay'),
        'recovery_notification_delay': module.params.get('recovery_notification_delay'),
        'acknowledgement_timeout': module.params.get('acknowledgement_timeout'),
        'freshness_threshold': module.params.get('freshness_threshold'),
        'flap_detection_enabled': module.params.get('flap_detection_enabled'),
        'low_flap_threshold': module.params.get('low_flap_threshold'),
        'high_flap_threshold': module.params.get('high_flap_threshold'),
        'event_handler_enabled': module.params.get('event_handler_enabled'),
        'event_handler_command_id': module.params.get('event_handler_command_id'),
        'event_handler_command_args': module.params.get('event_handler_command_args'),
        'note_url': module.params.get('note_url'),
        'note': module.params.get('note'),
        'action_url': module.params.get('action_url'),
        'icon_id': module.params.get('icon_id'),
        'icon_alternative': module.params.get('icon_alternative'),
        'comment': module.params.get('comment'),
        'is_activated': module.params.get('is_activated'),
        'categories': module.params.get('categories'),
        'groups': module.params.get('groups'),
        'templates': module.params.get('templates'),
        'macros': module.params.get('macros'),
    }

    host_data = {k: v for k, v in host_data.items() if v is not None}

    if module.params['state'] == 'create':

        result = create_host_configuration(api, host_data=host_data)
        module.exit_json(Created=True, result=result['id'])
        
    elif module.params['state'] == 'update':

        host_id = None
        if module.params['new_name']:
            host_data['name'] = module.params['new_name']
        else:
            host_data.pop('name', None)
        
        if module.params['host_id']:
            host_id = module.params['host_id']
        elif module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})
            hosts = find_all_host_configuration(api, query_parameters=filter_criteria)
            if len(hosts) != 1:
                module.fail_json(msg=f"Host {module.params['name']} multiple or not found for update.")
            host_id = hosts[0]['id']
        

        if host_id:
            if partially_update_host_configuration(api, host_id, host_data):
                module.exit_json(changed=True, result={"host_id": host_id, "status": "updated"})
        else:
            module.fail_json(msg="Host ID or name must be provided for update operation.")

    elif module.params['state'] == 'delete':
        host_id = None

        if module.params['host_id']:
            host_id = module.params['host_id']
        elif module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})

            hosts = find_all_host_configuration(api, query_parameters=filter_criteria)
            if len(hosts) != 1:
                module.fail_json(msg=f"Host {module.params['name']} multiple or not found for update. {len(hosts)}")
            host_id = hosts[0]['id']


        if host_id:
            if delete_host_configuration(api, host_id):
                module.exit_json(changed=True, result={"host_id": host_id, "status": "deleted"})
        else:
            module.fail_json(msg="Host ID or name must be provided for delete operation.")

if __name__ == '__main__':
    main()
