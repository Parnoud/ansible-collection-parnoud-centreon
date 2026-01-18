# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json


# CONFIGURATION


def list_all_host_severities(CentreonAPI_obj, params=None):
    """List of all host severity configurations."""
    return CentreonAPI_obj._get_all_paginated('GET', 'configuration/hosts/severities', params=params)


def create_host_severity(CentreonAPI_obj, hostseverity_data):
    """Create a host severity."""
    code, data = CentreonAPI_obj._request('POST', 'configuration/hosts/severities', data=hostseverity_data)
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
        raise Exception(f"Failed code {code}: {json.loads(data)['message']} {hostseverity_data}")


def delete_host_severity(CentreonAPI_obj, hostseverity_id: int):
    """Delete a host severity configuration"""
    code, data = CentreonAPI_obj._request('DELETE', f'configuration/hosts/severities/{hostseverity_id}')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to delete host severities: {json.loads(data)['message']}")


def get_host_severity(CentreonAPI_obj, hostseverity_id: int):
    """Get a host severity configuration"""
    code, data = CentreonAPI_obj._request('GET', f'configuration/hosts/severities/{hostseverity_id}')
    if code == 200:
        return json.loads(data)
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to get host severities: {json.loads(data)['message']}")


def update_host_severity(CentreonAPI_obj, hostseverity_id: int, hostseverity_data):
    """Update a host severity"""
    code, data = CentreonAPI_obj._request('PUT', f'configuration/hosts/severities/{hostseverity_id}', data=hostseverity_data)
    if code == 204:
        return True
    elif code == 400:
        raise Exception(f"Indicates that the server cannot or will not process the request: {json.loads(data)['message']}")
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    elif code == 409:
        raise Exception(f"Conflict: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to update host severities: {json.loads(data)['message']}")
