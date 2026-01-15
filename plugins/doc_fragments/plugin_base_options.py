# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


class ModuleDocFragment(object):
    # This document fragment serves as a partial base for all vmware plugins. It should be used in addition to the base fragment, vmware.vmware.base_options
    # since that contains the actual argument descriptions and defaults. This just defines the environment variables since plugins have something
    # like the module spec where that is usually done.
    DOCUMENTATION = r'''
options:
    hostname:
        env:
            - name: CENTREON_HOSTNAME
    username:
        env:
            - name: CENTREON_USERNAME
    password:
        env:
            - name: CENTREON_PASSWORD
    token:
        env:
            - name: CENTREON_TOKEN
    validate_certs:
        env:
            - name: CENTREON_VALIDATE_CERTS
    timeout:
        env:
            - name: CENTREON_TIMEOUT
'''
