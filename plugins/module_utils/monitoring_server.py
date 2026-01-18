# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json
from ansible_collections.parnoud.centreon.plugins.module_utils.centreon_api import CentreonAPI


def list_all_monitoring_server_configurations(api: CentreonAPI, params=None):
    """List all monitoring servers configurations."""
    return api._get_all_paginated('GET', 'configuration/monitoring-servers', params=params)


def generate_configuration_monitoring_server(api: CentreonAPI, monitoring_server_id: int) -> bool:
    """Generate and move the configuration files of the monitoring server."""
    code, data = api._request('GET', f'configuration/monitoring-servers/{monitoring_server_id}/generate')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to generate and move the configuration files of the monitoring server: {json.loads(data)['message']}")


def reload_configuration_monitoring_server(api: CentreonAPI, monitoring_server_id: int) -> bool:
    """Reload the configuration files of the monitoring server."""
    code, data = api._request('GET', f'configuration/monitoring-servers/{monitoring_server_id}/reload')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to reload the configuration files of the monitoring server: {json.loads(data)['message']}")


def generate_reload_configuration_monitoring_server(api: CentreonAPI, monitoring_server_id: int) -> bool:
    """Generate, move and reload the configuration files of the monitoring server."""
    code, data = api._request('GET', f'configuration/monitoring-servers/{monitoring_server_id}/generate-and-reload')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to generate, move and reload the configuration files of the monitoring server: {json.loads(data)['message']}")


def generate_configuration_all_monitoring_server(api: CentreonAPI) -> bool:
    """Generate and move the configuration files of the monitoring server."""
    code, data = api._request('GET', 'configuration/monitoring-servers/generate')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to generate and move the configuration files of the monitoring server: {json.loads(data)['message']}")


def reload_configuration_all_monitoring_server(api: CentreonAPI) -> bool:
    """Reload the configuration files for all monitoring servers."""
    code, data = api._request('GET', 'configuration/monitoring-servers/reload')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to reload the configuration files for all monitoring servers: {json.loads(data)['message']}")


def generate_reload_configuration_all_monitoring_server(api: CentreonAPI, monitoring_server_id: int) -> bool:
    """Generate, move and reload the configuration files for all monitoring servers."""
    code, data = api._request('GET', 'configuration/monitoring-servers/generate-and-reload')
    if code == 204:
        return True
    elif code == 403:
        raise Exception(f"Forbidden: {json.loads(data)['message']}")
    elif code == 404:
        raise Exception(f"Not Found: {json.loads(data)['message']}")
    else:
        raise Exception(f"Failed to generate, move and reload the configuration files for all monitoring servers: {json.loads(data)['message']}")
