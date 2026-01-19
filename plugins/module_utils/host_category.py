# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json


# CONFIGURATION


def list_host_caterogies(CentreonAPI_obj, params=None):
    """List of host category configurations"""
    return CentreonAPI_obj._get_all_paginated('GET', 'configuration/hosts/categories', params=params)


def create_host_category(CentreonAPI_obj, hostcategory_data):
    """Create a host category"""
    code, data = CentreonAPI_obj._request('POST', 'configuration/hosts/categories', data=hostcategory_data)
    if code == 201:
        return json.loads(data)
    elif code == 400:
        raise Exception(f"{json.loads(data)['message']}")
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    elif code == 409:
        raise Exception(f"Conflict: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed: {json.loads(data)['message']}")


def get_host_category(CentreonAPI_obj, hostcategory_id: int):
    """Get an existing host group."""
    code, data = CentreonAPI_obj._request('GET', f'configuration/hosts/categories/{hostcategory_id}')
    if code == 200:
        return json.loads(data)
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed: {json.loads(data)['message']}")


def update_host_category(CentreonAPI_obj, hostcategory_id: int, hostcategory_data):
    """Update a host category"""
    code, data = CentreonAPI_obj._request('PUT', f'configuration/hosts/categories/{hostcategory_id}', data=hostcategory_data)
    if code == 204:
        return True
    elif code == 400:
        raise Exception(f"Indicates that the server cannot or will not process the request : {json.loads(data)['message']}")
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    elif code == 409:
        raise Exception(f"Conflict: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed: {json.loads(data)['message']}")


def delete_host_category(CentreonAPI_obj, hostcategory_id: int):
    """Delete a host category configuration"""
    code, data = CentreonAPI_obj._request('DELETE', f'configuration/hosts/categories/{hostcategory_id}')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed: {json.loads(data)['message']}")


def list_all_real_time_host_caterogies(CentreonAPI_obj, params=None):
    """List of all host categories in real-time context"""
    return CentreonAPI_obj._get_all_paginated('GET', 'monitoring/hosts/categories', params=params)
