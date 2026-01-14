# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json


def find_all_host_template_configuration(CentreonAPI_obj, params=None):
    """Return all host template configurations."""
    return CentreonAPI_obj._get_all_paginated('GET', 'configuration/hosts/templates', params=params)