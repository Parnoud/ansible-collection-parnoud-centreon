# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json


def list_all_host_groups(CentreonAPI_obj, params=None):
    """Return all host group configurations."""
    return CentreonAPI_obj._get_all_paginated('GET', 'configuration/hosts/groups', params=params)


def add_host_group(CentreonAPI_obj, host_group_data):
    """Add a new host group configuration."""
    code, data = CentreonAPI_obj._request('POST', 'configuration/hosts/groups', data=host_group_data)
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
        raise Exception(f"Failed code {code}: {json.loads(data)['message']} {host_group_data}")


def get_host_groups(CentreonAPI_obj, host_group_id: int):
    """Get an existing host group."""
    code, data = CentreonAPI_obj._request('GET', f'configuration/hosts/groups/{host_group_id}')
    if code == 200:
        return json.loads(data)
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to get host group: {json.loads(data)['message']}")


def delete_host_group(CentreonAPI_obj, host_group_id: int):
    """Delete host group configuration by ID."""
    code, data = CentreonAPI_obj._request('DELETE', f'configuration/hosts/groups/{host_group_id}')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to delete host group: {json.loads(data)['message']}")


def update_host_group(CentreonAPI_obj, host_group_id: int, host_group_data):
    """Update host group."""
    code, data = CentreonAPI_obj._request('PUT', f'configuration/hosts/groups/{host_group_id}', data=host_group_data)
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
        raise Exception(f"Failed to update host group: {json.loads(data)['message']}")


def delete_multiple_host_groups(CentreonAPI_obj, host_group_ids: list):
    """Delete multiple host groups by their IDs."""
    code, data = CentreonAPI_obj._request('POST', 'configuration/hosts/groups/_delete', host_group_ids)
    if code == 200:
        return json.loads(data)
    elif code == 401:
        raise Exception(f"Unauthorized: {json.loads(data)['message']}")
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to delete host groups: {json.loads(data)['message']}")


def duplicate_multiple_host_groups(CentreonAPI_obj, ids, nb_duplicates: int):
    """Duplicate multiple host groups from configuration."""
    data_duplicate = {
        "ids": ids,
        "nb_duplicates": nb_duplicates
    }

    code, data = CentreonAPI_obj._request('POST', 'configuration/hosts/groups/_duplicate', data=data_duplicate)
    if code == 204:
        return json.loads(data)
    elif code == 401:
        raise Exception(f"Unauthorized: {json.loads(data)['message']}")
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to duplicate host groups code {code}: {json.loads(data)['message']} {data_duplicate}")


def list_all_host_groups_by_hostid(CentreonAPI_obj, host_id: int, params=None):
    """List all the host groups in real-time monitoring by host id."""
    return CentreonAPI_obj._get_all_paginated('GET', f'monitoring/hosts/{host_id}/hostgroups', params=params)


def list_all_host_groups(CentreonAPI_obj, params=None):
    """Return all host groups."""
    return CentreonAPI_obj._get_all_paginated('GET', 'monitoring/hosts/groups', params=params)
