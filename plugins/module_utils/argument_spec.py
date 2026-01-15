# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from ansible.module_utils.basic import env_fallback


def base_argument_spec():
    return dict(
        hostname=dict(
            type='str',
            required=False,
            fallback=(env_fallback, ['CENTREON_HOSTNAME']),
        ),
        username=dict(
            type='str',
            aliases=['user', 'admin'],
            required=False,
            fallback=(env_fallback, ['CENTREON_USERNAME'])
        ),
        password=dict(
            type='str',
            aliases=['pass', 'pwd'],
            required=False,
            no_log=True,
            fallback=(env_fallback, ['CENTREON_PASSWORD'])
        ),
        token=dict(
            type='str',
            no_log=True,
            fallback=(env_fallback, ['CENTREON_TOKEN'])
        ),
        validate_certs=dict(
            type='bool',
            required=False,
            default=False,
            fallback=(env_fallback, ['CENTREON_VALIDATE_CERTS'])
        ),
        timeout=dict(
            type='int',
            required=False,
            default=30,
            fallback=(env_fallback, ['CENTREON_TIMEOUT'])
        ),
    )
