# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

import json
import requests


class CentreonAPI:
    """CLass to interact with Centreon API v2."""

    def __init__(self, protocol=None, hostname=None, port=None, path=None, token=None, username=None, password=None, validate_certs=None, timeout=None):
        self.protocol = protocol if protocol else 'http'
        self.hostname = hostname if hostname else 'localhost'
        self.port = port if port else 80
        self.path = path if path else 'centreon/api/latest'
        self.validate_certs = validate_certs if validate_certs is not None else False
        self.timeout = timeout if timeout else 30
        self._build_url()

        if token:
            self.auth_method = 'token'
            self.auth_token = token
        elif username and password:
            self.auth_method = 'username_password'
            self.auth_username = username
            self.auth_password = password
        else:
            raise ValueError("Either token or username and password must be provided for authentication.")

        self.session_token = None
        self._authenticate()

    def _request(self, method, endpoint, data=None, params=None):
        """Request to centreon API v2 endpoint with given method, data and query parameters."""
        url = f"{self.base_url}/{endpoint}"

        response = requests.request(method=method, url=url, headers=self.headers, json=data, params=params, verify=self.validate_certs, timeout=self.timeout)
        return response.status_code, response.content

    def _authenticate(self):
        """Authenticate on centreon APIv2 with username/password or token."""
        if self.auth_method == 'token':
            self.headers = {
                'ContentType' : 'application/json',
                'X-AUTH-TOKEN' : self.auth_token
            }
            self.session_token = self.auth_token
        else:
            self.headers = {
                'ContentType' : 'application/json'
            }
            auth_data = {
                'security': {
                    'credentials': {
                        'login': self.auth_username,
                        'password': self.auth_password
                    }
                }
            }

            try:
                code, data = self._request(method='POST', endpoint='login', data=auth_data)
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
                params=query_parameters
            )

            if code == 403:
                raise Exception(f"Forbidden: {json.loads(data)['message']}")
            elif code != 200:
                raise Exception(f"Failed to get paginated data: {json.loads(data)['message']}")

            response = json.loads(data)

            all_results.extend(response['result'])
            if not response['result'] or len(all_results) >= response['meta']['total'] or response['meta']['total'] <= 100:
                break

            page += 1

        return all_results

    def _build_url(self):
        url = '{0}://{1}:{2}'.format(self.protocol, self.hostname, self.port)
        if self.path:
            url = '{0}/{1}'.format(url, self.path)
        self.base_url = url
