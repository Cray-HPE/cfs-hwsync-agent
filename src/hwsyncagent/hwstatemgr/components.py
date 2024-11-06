#
# MIT License
#
# (C) Copyright 2020-2024 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
"""
This is an HSM Component client, designed to interact with cray-smd/hsm/v1/State/Component endpoint.
"""

import logging
import json
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

from hwsyncagent.client import requests_retry_session
from . import ENDPOINT as BASE_ENDPOINT
from . import HWStateManagerException

LOGGER = logging.getLogger(__name__)
ENDPOINT = '%s/State/Components/' % BASE_ENDPOINT


def read_all_node_xnames(component_types=None):
    """
    Queries HSM for the full set of xname components that have been discovered;
    filtering entries down to xnames belonging to the component_types set.
    Return: A set of strings representing xnames.
    """
    if component_types is None:
        component_types = set(['Node', 'VirtualNode'])
    session = requests_retry_session()
    endpoint = '%s/State/Components/' % BASE_ENDPOINT
    try:
        response = session.get(endpoint)
    except ConnectionError as ce:
        LOGGER.error("Unable to contact HSM service: %s", ce)
        raise HWStateManagerException(ce) from ce
    try:
        response.raise_for_status()
    except (HTTPError, MaxRetryError) as hpe:
        LOGGER.error("Unexpected response from HSM: %s", response)
        raise HWStateManagerException(hpe) from hpe
    try:
        json_body = json.loads(response.text)
    except json.JSONDecodeError as jde:
        LOGGER.error("Non-JSON response from HSM: %s", response.text)
        raise HWStateManagerException(jde) from jde
    try:
        # Return the ID field for nodes which meet both of the following criteria:
        # - ID field is not empty
        # - Type field is in component_types
        return set([component['ID'] for component in json_body['Components']
                    if component['ID'] and component.get('Type', None) in component_types])
    except KeyError as ke:
        LOGGER.error("Unexpected API response from HSM")
        raise HWStateManagerException(ke) from ke
