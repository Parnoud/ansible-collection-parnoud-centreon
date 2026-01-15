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
    - Update a host in Centreon.
    - Delete a host in Centreon.
author: "Pierre ARNOUD (@parnoud)"
options:
    state:
        description: Desired state of the host.
        choices: ['create', 'delete', 'update', 'replace']
        default: 'create'
        type: str
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
        type: list
    templates:
        description: Templates associated with the host.
        required: false
        type: list
    macros:
        description: Macros associated with the host.
        required: false
        type: list
extends_documentation_fragment:
    - parnoud.centreon.base_options
'''

EXAMPLES = r'''

'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI
from ansible_collections.parnoud.centreon.plugins.module_utils.host import (
    delete_host_configuration,
    partially_update_host_configuration,
    find_all_host_configuration,
    create_host_configuration
)
from ansible_collections.parnoud.centreon.plugins.module_utils.host_group import list_all_host_groups_configuration
from ansible_collections.parnoud.centreon.plugins.module_utils.host_template import find_all_host_template_configuration
from ansible_collections.parnoud.centreon.plugins.module_utils.argument_spec import base_argument_spec


def manage_host(module):
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

    if host_data.get('groups'):
        new_groups = []
        for val in host_data['groups']:
            if isinstance(val, str):
                filter_criteria = {}
                filter_criteria['search'] = json.dumps({'name': val})
                host_groups = list_all_host_groups_configuration(api, params=filter_criteria)
                if len(host_groups) != 1:
                    return False, f"Host group {val} multiple or not found for update."
                host_group_id = host_groups[0]['id']
                new_groups.append(host_group_id)
            else:
                new_groups.append(val)
        host_data['groups'] = new_groups

    if host_data.get('templates'):
        new_templates = []
        for val in host_data['templates']:
            if isinstance(val, str):
                filter_criteria = {}
                filter_criteria['search'] = json.dumps({'name': val})
                hosts_templates = find_all_host_template_configuration(api, params=filter_criteria)
                if len(hosts_templates) != 1:
                    return False, f"Host template {val} multiple or not found for update."
                host_template_id = hosts_templates[0]['id']
                new_templates.append(host_template_id)
            else:
                new_templates.append(val)
        host_data['templates'] = new_templates

    if module.params['state'] == 'create':

        result = create_host_configuration(api, host_data=host_data)
        return True, result

    elif module.params['state'] == 'replace':

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
            hosts = find_all_host_configuration(api, params=filter_criteria)
            if len(hosts) != 1:
                return False, f"Host {module.params['name']} multiple or not found for update. {filter_criteria}"
            host_id = hosts[0]['id']

        if host_id:
            if partially_update_host_configuration(api, host_id, host_data):
                filter_criteria = {}
                filter_criteria['search'] = json.dumps({'id': host_id})
                return True, find_all_host_configuration(api, params=filter_criteria)
        else:
            return False, "Host ID or name must be provided for update operation."

    elif module.params['state'] == 'update':

        host_id = None
        current_host_data = None

        if module.params['new_name']:
            host_data['name'] = module.params['new_name']
        else:
            host_data.pop('name', None)

        if module.params['host_id']:
            host_id = module.params['host_id']

        elif module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})
            hosts = find_all_host_configuration(api, params=filter_criteria)
            if len(hosts) != 1:
                return False, f"Host {module.params['name']} multiple or not found for update. {filter_criteria}"
            host_id = hosts[0]['id']
            current_host_data = hosts[0]

        current_host_data.pop('id', None)
        current_host_data.pop('monitoring_server', None)

        current_host_data.pop('notification_timeperiod', None)
        current_host_data.pop('check_timeperiod', None)
        current_host_data.pop('severity', None)

        current_host_data["categories"] = [item["id"] for item in current_host_data["categories"]]
        if host_data.get('categories'):
            current_host_data["categories"] += list(host_data['categories'])

        current_host_data["groups"] = [item["id"] for item in current_host_data["groups"]]
        if host_data.get('groups'):
            current_host_data["groups"] += list(host_data['groups'])

        current_host_data["templates"] = [item["id"] for item in current_host_data["templates"]]
        if host_data.get('templates'):
            current_host_data["templates"] += list(host_data['templates'])

        if host_id:
            if partially_update_host_configuration(api, host_id, current_host_data):
                filter_criteria = {}
                filter_criteria['search'] = json.dumps({'id': host_id})
                return True, find_all_host_configuration(api, params=filter_criteria)
        else:
            return False, "Host ID or name must be provided for update operation."

    elif module.params['state'] == 'delete':
        host_id = None

        if module.params['host_id']:
            host_id = module.params['host_id']
        elif module.params['name']:
            filter_criteria = {}
            filter_criteria['search'] = json.dumps({'name': module.params['name']})

            hosts = find_all_host_configuration(api, params=filter_criteria)
            if len(hosts) == 0:
                return True, hosts
            elif len(hosts) >= 2:
                return False, f"Host {module.params['name']} multiple for update. {len(hosts)}"

            host_id = hosts[0]['id']

        if host_id:
            if delete_host_configuration(api, host_id):
                return True, hosts[0]
        else:
            return False, "Host ID or name must be provided for delete operation."


def main():
    argument_spec = base_argument_spec()
    argument_spec.update(
        state=dict(type='str', choices=['create', 'delete', 'update', 'replace'], default='create'),
        monitoring_server_id=dict(type='int'),
        host_id=dict(type='int', default=None),
        name=dict(type='str', default=None),
        new_name=dict(type='str', default=None),
        address=dict(type='str', default=None),
        alias=dict(type='str', default=None),
        snmp_community=dict(type='str', default=None),
        snmp_version=dict(type='str', choices=['1', '2c', '3'], default=None),
        geo_coords=dict(type='str', default=None),
        timezone_id=dict(type='int', default=None),
        severity_id=dict(type='int', default=None),
        check_command_id=dict(type='int', default=None),
        check_command_args=dict(type='dict', default=None),
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
        event_handler_command_args=dict(type='dict', default=None),
        note_url=dict(type='str', default=None),
        note=dict(type='str', default=None),
        action_url=dict(type='str', default=None),
        icon_id=dict(type='int', default=None),
        icon_alternative=dict(type='str', default=None),
        comment=dict(type='str', default=None),
        is_activated=dict(type='bool', default=None),
        categories=dict(type='list', default=None),
        groups=dict(type='list', default=None),
        templates=dict(type='list', default=None),
        macros=dict(type='list', default=None),
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    return_type, data = manage_host(module)
    if return_type:
        module.exit_json(changed=False, data=data)
    else:
        module.fail_json(msg=data)


if __name__ == '__main__':
    main()
