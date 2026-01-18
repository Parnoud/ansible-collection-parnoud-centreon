# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = r'''
---
module: partially_update_host_configuration
short_description: Partially update a host configuration.
description:
    - Update a host configuration with givens parameters by host_id
author: "Pierre ARNOUD (@parnoud)"
options:
    host_id:
        description: Host ID
        required: true
        type: int
    monitoring_server_id:
        description: ID of the host's monitoring server
        type: int
        default: null
    name:
        description: Host name
        type: str
        default: null
    address:
        description: IP or domain of the host
        type: str
        default: null
    alias:
        description: Host alias
        required: false
        type: str
        default: null
    snmp_community:
        description: Community of the SNMP agent
        required: false
        type: str
        default: null
    snmp_version:
        description: Version of the SNMP agent.
        required: false
        type: str
        choices: ['1', '2c', '3']
        default: null
    geo_coords:
        description: Geographic coordinates of the host
        required: false
        type: str
        default: null
    timezone_id:
        description: Timezone ID
        required: false
        type: int
        default: null
    severity_id:
        description: Severity ID
        required: false
        type: int
        default: null
    check_command_id:
        description: Check command ID. Must be of type 'Check'.
        required: false
        type: int
        default: null
    check_command_args:
        description: Check command arguments
        required: false
        type: list
        elements: str
        default: null
    check_timeperiod_id:
        description: Check command timeperiod ID
        required: false
        type: int
        default: null
    max_check_attempts:
        description: Define the number of times that the monitoring engine will retry the host check command if it returns any non-OK state
        required: false
        type: int
        default: null
    normal_check_interval:
        description: Define the number of 'time units' between regularly scheduled checks of the host.
        required: false
        type: int
        default: null
    retry_check_interval:
        description: Define the number of "time units" to wait before scheduling a re-check for this host after a non-UP state was detected.
        required: false
        type: int
        default: null
    active_check_enabled:
        description: Indicates whether active checks are enabled or not
        required: false
        type: int
        choices: [0, 1, 2]
        default: null
    passive_check_enabled:
        description: Indicates whether passive checks are enabled or not
        required: false
        type: int
        choices: [0, 1, 2]
        default: null
    notifications_enabled:
        description: Specify whether notifications for this host are enabled or not
        required: false
        type: int
        choices: [0, 1, 2]
        default: null
    notification_options:
        description: Define the states of the host for which notifications should be sent out.
        required: false
        type: int
        choices: [0, 1, 2, 4, 8, 16]
        default: null
    notification_interval:
        description: Define the number of "time units" to wait before re-notifying a contact that this host is still down or unreachable.
        required: false
        type: int
        default: null
    notification_timeperiod_id:
        description: Notification timeperiod ID
        required: false
        type: int
        default: null
    add_inherited_contact_group:
        description: Only used when notification inheritance for hosts and services is set to vertical inheritance only.
        required: false
        type: bool
        default: null
    add_inherited_contact:
        description: Only used when notification inheritance for hosts and services is set to vertical inheritance only.
        required: false
        type: bool
    first_notification_delay:
        description: Define the number of "time units" to wait before sending out the first alert notification when this host enters a non-UP state.
        required: false
        type: int
        default: null
    recovery_notification_delay:
        description: Define the number of "time units" to wait before sending out the recovery notification when this host enters an UP state.
        required: false
        type: int
        default: null
    acknowledgement_timeout:
        description: Specify a duration of acknowledgement for this host.
        required: false
        type: int
        default: null
    freshness_threshold:
        description: Specify the freshness threshold (in seconds) for this host.
        required: false
        type: int
        default: null
    flap_detection_enabled:
        description: Indicates whether the flap detection is enabled or not
        required: false
        type: int
        choices: [0, 1, 2]
        default: null
    low_flap_threshold:
        description: Specify the low state change threshold used in flap detection for this host
        required: false
        type: int
        default: null
    high_flap_threshold:
        description: Specify the high state change threshold used in flap detection for this host
        required: false
        type: int
        default: null
    event_handler_enabled:
        description: Indicates whether the event handler is enabled or not
        required: false
        type: int
        choices: [0, 1, 2]
        default: null
    event_handler_command_id:
        description: Event handler command ID
        required: false
        type: int
        default: null
    event_handler_command_args:
        description: Event handler command arguments
        required: false
        type: list
        elements: str
        default: null
    note_url:
        description: Define an optional URL that can be used to provide more information about the host.
        required: false
        type: str
        default: null
    note:
        description: Define an optional note.
        required: false
        type: str
        default: null
    action_url:
        description: Define an optional URL that can be used to provide more actions to be performed on the host.
        required: false
        type: str
        default: null
    icon_id:
        description: Define the ID of the image that should be associated with this host
        required: false
        type: int
        default: null
    icon_alternative:
        description: Define an optional string that is used as alternative description for the icon
        required: false
        type: str
        default: null
    comment:
        description: Host comments
        required: false
        type: str
        default: null
    is_activated:
        description: Indicates whether the host is activated or not
        required: false
        type: bool
        default: null
    categories:
        description: Define the host category IDs that should be associated with this host
        required: false
        type: list
        elements: int
        default: null
    groups:
        description: Define the host group IDs that should be associated with this host
        required: false
        type: list
        elements: int
        default: null
    templates:
        description: Define the parent host template IDs that should be associated with this host.
        required: false
        type: list
        elements: int
        default: null
    macros:
        description: Host macros defined for the host (directly or through a template or command inheritance)
        required: false
        type: list
        elements: dict
        default: null
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''
---
- name: Update host configuration by id
  parnoud.centreon.delete_host_configuration:
        hostname: centreon.com/centreon/api/latest
        username: user
        password: pass
        host_id: 32
        name: new-host-name
'''

RETURN = r'''
---
host_id:
    description: 0 to indicate delete
    returned: success
    type: int
    sample : 0
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec
from ansible_collections.parnoud.centreon.plugins.module_utils.host import partially_update_host_configuration


def partially_update_host_configuration_with_parameters(module):
    """entry point for module execution"""

    api = CentreonAPI(
        hostname=module.params.get('hostname'),
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

    if partially_update_host_configuration(api, host_id=module.params.get('host_id'), host_data=host_data):
        return True, 0
    else:
        return False, module.params.get('host_id')


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        host_id=dict(type='int', required=True),
        monitoring_server_id=dict(type='int', default=None),
        name=dict(type='str', default=None),
        address=dict(type='str', default=None),
        alias=dict(type='str', default=None),
        snmp_community=dict(type='str', default=None),
        snmp_version=dict(type='str', choices=['1', '2c', '3'], default=None),
        geo_coords=dict(type='str', default=None),
        timezone_id=dict(type='int', default=None),
        severity_id=dict(type='int', default=None),
        check_command_id=dict(type='int', default=None),
        check_command_args=dict(type='list', elements='str', default=None),
        check_timeperiod_id=dict(type='int', default=None),
        max_check_attempts=dict(type='int', default=None),
        normal_check_interval=dict(type='int', default=None),
        retry_check_interval=dict(type='int', default=None),
        active_check_enabled=dict(type='int', choices=[0, 1, 2], default=None),
        passive_check_enabled=dict(type='int', choices=[0, 1, 2], default=None),
        notifications_enabled=dict(type='int', choices=[0, 1, 2], default=None),
        notification_options=dict(type='int', choices=[0, 1, 2, 4, 8, 16], default=None),
        notification_interval=dict(type='int', default=None),
        notification_timeperiod_id=dict(type='int', default=None),
        add_inherited_contact_group=dict(type='bool', default=None),
        add_inherited_contact=dict(type='bool', default=None),
        first_notification_delay=dict(type='int', default=None),
        recovery_notification_delay=dict(type='int', default=None),
        acknowledgement_timeout=dict(type='int', default=None),
        freshness_threshold=dict(type='int', default=None),
        flap_detection_enabled=dict(type='int', choices=[0, 1, 2], default=None),
        low_flap_threshold=dict(type='int', default=None),
        high_flap_threshold=dict(type='int', default=None),
        event_handler_enabled=dict(type='int', choices=[0, 1, 2], default=None),
        event_handler_command_id=dict(type='int', default=None),
        event_handler_command_args=dict(type='list', elements='str', default=None),
        note_url=dict(type='str', default=None),
        note=dict(type='str', default=None),
        action_url=dict(type='str', default=None),
        icon_id=dict(type='int', default=None),
        icon_alternative=dict(type='str', default=None),
        comment=dict(type='str', default=None),
        is_activated=dict(type='bool', default=None),
        categories=dict(type='list', elements='int', default=None),
        groups=dict(type='list', elements='int', default=None),
        templates=dict(type='list', elements='int', default=None),
        macros=dict(type='list', elements='dict', default=None)
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    status, object = partially_update_host_configuration_with_parameters(module)
    if status:
        module.exit_json(succes=True, object=object)
    else:
        module.fail_json(object=[])


if __name__ == '__main__':
    main()
