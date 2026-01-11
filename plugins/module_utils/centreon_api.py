# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.six.moves.urllib.parse import urlencode
import json
import os


class CentreonAPI:
    """CLass to interact with Centreon API v2."""

    def __init__(self, protocol="https", hostname=None, port=443, path="centreon", token=None, username=None, password=None, validate_certs=True, timeout=30):
        self.protocol = protocol or os.getenv('CENTREON_PROTOCOL')
        self.hostname = hostname or os.getenv('CENTREON_HOSTNAME')
        self.port = port or os.getenv('CENTREON_PORT')
        self.path = path or os.getenv('CENTREON_PATH')
        self.validate_certs = validate_certs or os.getenv('CENTREON_VALIDATE_CERTS')
        self.timeout = timeout or os.getenv('CENTREON_TIMEOUT')
        self.headers = {'Content-Type': 'application/json'}
        self.base_url = f"{self.protocol}://{self.hostname}:{self.port}/{self.path}/api/latest"

        if token and (username or password):
            raise ValueError("Provide either a token or username/password, not both.")
        if not token and not (username or password):
            env_token = os.getenv('CENTREON_TOKEN')
            env_username = os.getenv('CENTREON_USERNAME')
            env_password = os.getenv('CENTREON_PASSWORD')
            if env_token and (env_username or env_password):
                raise ValueError("Ambiguous authentication in environment: provide either a token or username/password.")
            if env_token:
                token = env_token
            elif env_username and env_password:
                username = env_username
                password = env_password
            else:
                raise ValueError("No authentication method provided (token or username/password).")

        if token:
            self.auth_method = 'token'
            self.auth_token = token
        else:
            self.auth_method = 'username_password'
            self.auth_username = username
            self.auth_password = password

        self.session_token = None
        self._authenticate()

    def _request(self, method, endpoint, data=None, query_parameters=None):
        """Request to centreon API v2 endpoint with given method, data and query parameters."""
        url = f"{self.base_url}/{endpoint}"

        # Ajout des paramètres à l'URL si présents
        if query_parameters:
            query_string = urlencode(query_parameters)
            url = f"{url}?{query_string}"

        try:
            response = open_url(
                url=url,
                headers=self.headers,
                method=method,
                data=json.dumps(data) if data else None,
                validate_certs=self.validate_certs,
                timeout=self.timeout
            )
            return response.getcode(), response.read()
        except HTTPError as e:
            return e.code, e.read()
        except (URLError, ConnectionError, SSLValidationError) as e:
            return 0, str(e)

    def _authenticate(self):
        """Authentucate on centreon APIv2 with username/password or token."""
        if self.auth_method == 'token':
            # Authentification par token
            self.headers = {
                'ContentType' : 'application/json',
                'X-AUTH-TOKEN' : self.auth_token
            }
            self.session_token = self.auth_token
        else:
            # Authentification par login/mot de passe
            auth_data = {
                'security': {
                    'credentials': {
                        'login': self.auth_username,
                        'password': self.auth_password
                    }
                }
            }
            try:
                code, data = self._request('POST', 'login', auth_data)
                if code == 200:
                    response = json.loads(data)
                    self.session_token = response['security']['token']
                    self.headers = {
                        'ContentType' : 'application/json',
                        'X-AUTH-TOKEN' : self.session_token
                    }
                else:
                    raise Exception(f"Authentication failed: {data}")
            except Exception as e:
                raise Exception(f"Failed to authenticate: {str(e)}")

    def _get_all_paginated(self, method, endpoint, params=None):
        """Return all data from a paginated endpoint."""
        all_results = []
        page = 1
        query_parameters = {}
        while True:
            pages = {
                'page': page
            }
            limites = {
                'limit': 100
            }

            query_parameters.update(pages)
            query_parameters.update(limites)

            if params:
                query_parameters.update(params)

            code, data = self._request(
                method=method,
                endpoint=endpoint,
                query_parameters=query_parameters
            )

            if code != 200:
                raise Exception(f"Failed to get data (page {page}): {data}")

            response = json.loads(data)
            all_results.extend(response['result'])

            if not response['result'] or page >= response['meta']['total'] / 100 + 1:
                break

            page += 1

        return all_results

    def find_all_host_configuration(self, query_parameters=None):
        """Return host configurations filtered by query parameters."""
        data = self._get_all_paginated('GET', 'configuration/hosts', params=query_parameters)
        return data

    def get_host(self, host_id: int):
        """Get host configuration by ID."""
        code, data = self._request('GET', f'configuration/hosts/{host_id}')
        if code == 200:
            return json.loads(data)
        elif code == 404:
            return None
        else:
            raise Exception(f"Failed to get host: {data}")

    def create_host(self, host_data):
        """Crée un nouvel hôte."""
        code, data = self._request('POST', 'configuration/hosts', host_data)
        if code == 201:
            return json.loads(data)
        else:
            raise Exception(f"Failed to create host: {data}")
