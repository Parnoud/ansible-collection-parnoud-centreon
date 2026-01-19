# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json


def delete_service_category(CentreonAPI_obj, hostcategory_id: int):
    """Delete a service category configuration"""
    code, data = CentreonAPI_obj._request('DELETE', f'configuration/services/categories/{hostcategory_id}')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed: {json.loads(data)['message']}")
