# -*- coding: utf-8 -*-

#
# minju centreon Ansible Modules
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
    """Classe utilitaire pour interagir avec l'API v2 de Centreon."""

    def __init__(self, hostname=None, token=None, username=None, password=None, validate_certs=True, timeout=30):
        # Récupération depuis les variables d'environnement si non fourni
        self.hostname = hostname or os.getenv('CENTREON_HOSTNAME')
        self.validate_certs = validate_certs or os.getenv('CENTREON_VALIDATE_CERTS')
        self.timeout = timeout or os.getenv('CENTREON_TIMEOUT')
        self.headers = {'Content-Type': 'application/json'}
        self.base_url = f"https://{self.hostname}/api/latest"

        # Gestion de l'authentification
        if token and (username or password):
            raise ValueError("Provide either a token or username/password, not both.")
        if not token and not (username or password):
            # On essaie depuis l'environnement
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

    def _request(self, method, endpoint, data=None, params=None):
        """Effectue une requête HTTP vers l'API Centreon."""
        url = f"{self.base_url}/{endpoint}"

        # Ajout des paramètres à l'URL si présents
        if params:
            query_string = urlencode(params)
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
        """Authentification par token ou login/mot de passe."""
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

    def get_hosts(self):
        """Récupère la liste des hôtes."""
        data = self._get_all_paginated('GET', 'configuration/hosts')
        return data

    def _get_all_paginated(self, method, endpoint, limit=100):
        """Récupère tous les résultats paginés d'un endpoint."""
        all_results = []
        page = 1
        while True:
            code, data = self._request(
                method=method,
                endpoint=endpoint,
                params={'page': page, 'limit': limit}
            )
            if code != 200:
                raise Exception(f"Failed to get data (page {page}): {data}")

            response = json.loads(data)
            all_results.extend(response['result'])

            if not response['result'] or page >= response['meta']['total'] / limit + 1:
                break

            page += 1

        return all_results
