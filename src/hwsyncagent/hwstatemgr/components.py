'''
This is an HSM Component client, designed to interact with cray-smd/hsm/v1/State/Component endpoint.

Created on Jan 30, 2020

@author: jsl
Copyright 2020, Cray Inc., A Hewlett Packard Enterprise Company
'''

import logging
import json
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

from hwsyncagent.client import requests_retry_session
from . import ENDPOINT as BASE_ENDPOINT
from . import HWStateManagerException

LOGGER = logging.getLogger(__name__)
ENDPOINT = '%s/State/Components/' % (BASE_ENDPOINT)


def read_all_node_xnames():
    """
    Queries HSM for the full set of xname components that
    have been discovered; return these as a set.
    """
    client = requests_retry_session()
    try:
        response = client.get(ENDPOINT)
    except ConnectionError as ce:
        LOGGER.error("Unable to contact HSM service: %s", ce)
        raise HWStateManagerException(ce)
    try:
        response.raise_for_status()
    except (HTTPError, MaxRetryError) as hpe:
        LOGGER.error("Unexpected response from HSM: %s", response)
        raise HWStateManagerException(hpe)
    try:
        json_body = json.loads(response.text)
    except json.JSONDecodeError as jde:
        LOGGER.error("Non-JSON response from HSM: %s", response.text)
        raise HWStateManagerException(jde)
    try:
        return set([component['ID'] for component in json_body['Components']
                    if component.get('Type', None) == 'Node'])
    except KeyError as ke:
        LOGGER.error("Unexpected API response from HSM")
        raise HWStateManagerException(ke)
