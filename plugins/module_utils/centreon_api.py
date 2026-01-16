# -*- coding: utf-8 -*-

#
# parnoud centreon Ansible Modules
# Version 1.0.0
# Copyright (C) All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


DOCUMENTATION = '''
---
author:
- ARNOUD Pierre (@parnoud)
name : centreon_api
short_description: CentreonAPI Plugin for Centreon REST API V2
description:
  - This CentreonAPI plugin provides methods to connect to centreon over a HTTP(S)-based APIs v2.
'''

import json

try:
    import requests
except ImportError as imp_exc:
    ANOTHER_LIBRARY_IMPORT_ERROR = imp_exc
else:
    ANOTHER_LIBRARY_IMPORT_ERROR = None


class CentreonAPI:
    """CLass to interact with Centreon API v2."""

    def __init__(self,
                 hostname: str = None,
                 token: str = None,
                 username: str = None,
                 password: str = None,
                 validate_certs: bool = False,
                 timeout: int = 30):
        self.hostname = hostname
        self.token = token
        self.validate_certs = validate_certs
        self.timeout = timeout

        if ANOTHER_LIBRARY_IMPORT_ERROR:
            raise ValueError('another_library must be installed to use this plugin') from ANOTHER_LIBRARY_IMPORT_ERROR

        if hostname is None:
            raise ValueError('Hostname is required')

        if self.token:
            self.headers = {
                'ContentType' : 'application/json',
                'X-AUTH-TOKEN' : self.token
            }
        elif username and password:
            self.login(username=username, password=password)
        else:
            raise ValueError("Either token or username and password must be provided for authentication.")

    def _request(self,
                 method: str,
                 endpoint: str,
                 data: dict = None,
                 params: dict = None) -> tuple[int, bytes]:
        """Request to centreon API v2 endpoint with given method, data and query parameters."""
        url = f"{self.hostname}/{endpoint}"

        response = requests.request(method=method, url=url, headers=self.headers, json=data, params=params, verify=self.validate_certs, timeout=self.timeout)
        return response.status_code, response.content

    def _get_all_paginated(self,
                           method: str,
                           endpoint: str,
                           params = None) -> dict:
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

    def login(self,
              username: str,
              password: str):
        """Entry point to retrieve an authentication token."""
        self.headers = {
            'ContentType' : 'application/json'
        }
        data = {
            'security': {
                'credentials': {
                    'login': username,
                    'password': password
                }
            }
        }

        code, data = self._request(method='POST', endpoint='login', data=data)
        if code == 200:
            response = json.loads(data)
            self.token = response['security']['token']
            self.headers = {
                'ContentType' : 'application/json',
                'X-AUTH-TOKEN' : self.token
            }
        elif code == 400:
            raise Exception(f"Server cannot or will not process the request : {json.loads(data)['message']}")
        elif code == 401:
            raise Exception(f"Unauthorized : {json.loads(data)['message']}")
        else:
            raise Exception(f"Failed: {json.loads(data)['message']}")

    def logout(self):
        """Entry point to delete an existing authentication token."""
        code, data = self._request(method='GET', endpoint='logout')
        if code == 200:
            return json.loads(data)
        elif code == 403:
            raise Exception(f"Forbidden : {json.loads(data)['message']}")
        else:
            raise Exception(f"Failed: {json.loads(data)['message']}")
