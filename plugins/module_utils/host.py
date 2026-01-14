# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json


def delete_host_configuration(CentreonAPI_obj, host_id: int):
    """Delete host configuration by ID."""
    code, data = CentreonAPI_obj._request('DELETE', f'configuration/hosts/{host_id}')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to delete host: {json.loads(data)['message']}")


def partially_update_host_configuration(CentreonAPI_obj, host_id, host_data):
    """Partially update a host configuration"""
    code, data = CentreonAPI_obj._request('PATCH', f'configuration/hosts/{host_id}', data=host_data)
    if code == 204:
        return True
    elif code == 400:
        raise Exception(f"Indicates that the server cannot or will not process the \
                        request due to something that is perceived to be a client error: {json.loads(data)['message']}")
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    elif code == 409:
        raise Exception(f"Conflict: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to partially update host: {json.loads(data)['message']}")


def find_all_host_configuration(CentreonAPI_obj, params=None):
    """Return host configurations filtered by query parameters."""
    return CentreonAPI_obj._get_all_paginated('GET', 'configuration/hosts', params=params)


def create_host_configuration(CentreonAPI_obj, host_data):
    """Create a host configuration"""
    code, data = CentreonAPI_obj._request('POST', 'configuration/hosts', host_data)
    if code == 201:
        return json.loads(data)
    elif code == 400:
        raise Exception(f"Indicates that the server cannot or will not process the \
                        request due to something that is perceived to be a client error: {json.loads(data)['message']}")
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    elif code == 409:
        raise Exception(f"Conflict: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed: {json.loads(data)['message']}")


def get_host(CentreonAPI_obj, host_id: int):
    """Get host configuration by ID."""
    code, data = CentreonAPI_obj._request('GET', f'configuration/hosts/{host_id}')
    if code == 200:
        return json.loads(data)
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed: {json.loads(data)['message']}")


def count_hosts_by_status(CentreonAPI_obj, params=None):
    """Count hosts by their status (UP/DOWN/UNREACHABLE/PENDING)."""
    code, data = CentreonAPI_obj._request('GET', 'monitoring/hosts/count', params=params)
    if code == 200:
        response = json.loads(data)
        return response.get('count', 0)
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to count hosts: {json.loads(data)['message']}")
