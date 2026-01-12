# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

DOCUMENTATION = r'''
---
module: centreon_host
short_description: Manage hosts in Centreon via API v2
description:
    - Add, remove, or modify hosts in Centreon.
author: "Pierre ARNOUD (@parnoud)"
options:
    hostname:
        description: URL to Centreon API v2.
        required: true
        type: str
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
    name:
        description: Host name.
        required: true
        type: str
    state:
        description: Desired state of the host.
        choices: ['present', 'absent']
        default: 'present'
        type: str
    alias:
        description: Host alias.
        type: str
    address:
        description: Host address.
        type: str
    hostgroups:
        description: List of hostgroup IDs.
        type: list
        elements: int
    templates:
        description: List of template IDs.
        type: list
        elements: int
    categories:
        description: List of category IDs.
        type: list
        elements: int
    poller_id:
        description: Poller ID.
        type: int
    check_command:
        description: Check command.
        type: str
    max_check_attempts:
        description: Max check attempts.
        type: int
    notes:
        description: Host notes.
        type: str
    enabled:
        description: Enable or disable the host.
        type: bool
        default: true
'''

EXAMPLES = r'''
- name: Add a host
  parnoud.centreon.centreon_host:
    hostname: "centreon.example.com"
    token: "ton_token"
    name: "mon_serveur"
    state: present
    alias: "Mon Serveur"
    address: "192.168.1.10"
    hostgroups: [1, 2]
    templates: [3]
    poller_id: 1
    check_command: "check-host-alive"
    max_check_attempts: 3

- name: Remove a host
  parnoud.centreon.centreon_host:
    hostname: "centreon.example.com"
    token: "ton_token"
    name: "mon_serveur"
    state: absent
'''

import os
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI


def main():
    module = AnsibleModule(
        argument_spec=dict(
            protocol=dict(required=False, type='str'),
            hostname=dict(required=False, type='str'),
            port=dict(required=False, type='int'),
            path=dict(required=False, type='str'),
            token=dict(required=False, type='str', no_log=True),
            username=dict(required=False, type='str'),
            password=dict(required=False, type='str', no_log=True),
            validate_certs=dict(required=False, type='bool'),
            timeout=dict(required=False, type='int'),
            name=dict(required=True, type='str'),
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            alias=dict(type='str'),
            address=dict(type='str'),
            hostgroups=dict(type='list', elements='int'),
            templates=dict(type='list', elements='int'),
            categories=dict(type='list', elements='int'),
            poller_id=dict(type='int'),
            check_command=dict(type='str'),
            max_check_attempts=dict(type='int'),
            notes=dict(type='str'),
            enabled=dict(type='bool', default=True),
        ),
        supports_check_mode=True,
        required_one_of=[['token', 'username', 'password']],
        mutually_exclusive=[['token', 'username'], ['token', 'password']],
    )

    protocol = module.params['protocol'] or os.getenv('CENTREON_PROTOCOL')
    hostname = module.params['hostname'] or os.getenv('CENTREON_HOSTNAME')
    port = module.params['port'] or os.getenv('CENTREON_PORT')
    path = module.params['path'] or os.getenv('CENTREON_PATH')
    token = module.params['token'] or os.getenv('CENTREON_TOKEN')
    username = module.params['username'] or os.getenv('CENTREON_USERNAME')
    password = module.params['password'] or os.getenv('CENTREON_PASSWORD')
    name = module.params['name']
    state = module.params['state']
    alias = module.params.get('alias')
    address = module.params.get('address')
    hostgroups = module.params.get('hostgroups', [])
    templates = module.params.get('templates', [])
    categories = module.params.get('categories', [])
    poller_id = module.params.get('poller_id')
    check_command = module.params.get('check_command')
    max_check_attempts = module.params.get('max_check_attempts')
    notes = module.params.get('notes')
    enabled = module.params.get('enabled')

    try:
        api = CentreonAPI(hostname=hostname, protocol=protocol, port=port, path=path, token=token, username=username, password=password)

        # Vérifie si l'hôte existe
        existing_host = None
        try:
            existing_host = api.get_host(name)
        except Exception:
            pass

        if state == 'present':
            if not existing_host:
                # Crée l'hôte
                host_data = {
                    'name': name,
                    'alias': alias,
                    'address': address,
                    'hostgroups': hostgroups,
                    'templates': templates,
                    'categories': categories,
                    'poller_id': poller_id,
                    'check_command': {'id': check_command} if check_command else None,
                    'max_check_attempts': max_check_attempts,
                    'notes': notes,
                    'enabled': enabled,
                }
                # Nettoie les champs None
                host_data = {k: v for k, v in host_data.items() if v is not None}
                api.create_host(host_data)
                module.exit_json(changed=True, msg=f"Host {name} created.")
            else:
                # Met à jour l'hôte si nécessaire
                needs_update = False
                update_data = {}

                if alias and existing_host.get('alias') != alias:
                    update_data['alias'] = alias
                    needs_update = True
                if address and existing_host.get('address') != address:
                    update_data['address'] = address
                    needs_update = True
                if hostgroups and set(existing_host.get('hostgroups', [])) != set(hostgroups):
                    update_data['hostgroups'] = hostgroups
                    needs_update = True
                if templates and set(existing_host.get('templates', [])) != set(templates):
                    update_data['templates'] = templates
                    needs_update = True
                if categories and set(existing_host.get('categories', [])) != set(categories):
                    update_data['categories'] = categories
                    needs_update = True
                if poller_id and existing_host.get('poller_id') != poller_id:
                    update_data['poller_id'] = poller_id
                    needs_update = True
                if check_command and existing_host.get('check_command', {}).get('id') != check_command:
                    update_data['check_command'] = {'id': check_command}
                    needs_update = True
                if max_check_attempts and existing_host.get('max_check_attempts') != max_check_attempts:
                    update_data['max_check_attempts'] = max_check_attempts
                    needs_update = True
                if notes and existing_host.get('notes') != notes:
                    update_data['notes'] = notes
                    needs_update = True
                if enabled is not None and existing_host.get('enabled') != enabled:
                    update_data['enabled'] = enabled
                    needs_update = True

                if needs_update:
                    api.update_host(name, update_data)
                    module.exit_json(changed=True, msg=f"Host {name} updated.")
                else:
                    module.exit_json(changed=False, msg=f"Host {name} already up to date.")

        elif state == 'absent':
            if existing_host:
                api.delete_host(name)
                module.exit_json(changed=True, msg=f"Host {name} deleted.")
            else:
                module.exit_json(changed=False, msg=f"Host {name} does not exist.")

    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
