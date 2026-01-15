# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
notes:
  - All modules require a token to acces to Centreon APIv2
  - All modules require a account with API access
options:
  hostname:
    description:
      - The complete URL to acces APIv2.
      - If the value is not specified in the task, the value of environment variable E(CENTREON_HOSTNAME) will be used instead.
    type: str
  username:
    description:
      - The Centreon username.
      - If the value is not specified in the task, the value of environment variable E(CENTREON_USERNAME) will be used instead.
    type: str
    aliases: [ admin, user ]
  password:
    description:
      - The Centreon password.
      - If the value is not specified in the task, the value of environment variable E(CENTREON_PASSWORD) will be used instead.
    type: str
    aliases: [ pass, pwd ]
  token:
    description:
      - The Centreon account token.
      - If the value is not specified in the task, the value of environment variable E(CENTREON_TOKEN) will be used instead.
    type: str
  validate_certs:
    description:
      - Allows connection when SSL certificates are not valid. Set to V(false) when certificates are not trusted.
      - If the value is not specified in the task, the value of environment variable E(CENTREON_VALIDATE_CERTS) will be used instead.
    type: bool
    default: False
  timeout:
    description:
    - The timeout time in sec.
    - If the value is not specified in the task, the value of environment variable E(CENTREON_TIMEOUT) will be used instead.
    type: int
    required: false
    default: 30
'''
