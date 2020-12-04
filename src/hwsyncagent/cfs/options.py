'''
The CFS API contains options that are pertinent to how the HWSync Agent
should operate. This module allows us to read those options from the API.

Created on Feb 4, 2020

@author: jsl
Copyright 2020, Cray Inc., A Hewlett Packard Enterprise Company
'''

import logging
import json
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

from hwsyncagent.client import requests_retry_session
from . import ENDPOINT as BASE_ENDPOINT, CFSException

LOGGER = logging.getLogger(__name__)
ENDPOINT = "%s/%s" % (BASE_ENDPOINT, __name__.lower().split('.')[-1])


def read_options():
    session = requests_retry_session()
    try:
        response = session.get(ENDPOINT)
    except (ConnectionError, MaxRetryError) as ce:
        LOGGER.error("Unable to connect to CFS.")
        raise CFSException(ce)
    try:
        response.raise_for_status()
    except HTTPError as hpe:
        LOGGER.error("Unexptected response from CFS.")
        raise CFSException(hpe)
    try:
        return json.loads(response.text)
    except json.JSONDecodeError as jde:
        LOGGER.error("Non-JSON response from CFS.")
        raise CFSException(jde)


def patch_options(obj):
    """
    Performs a patch operation on the API to register a default.

    obj is a dictionary containing key value pairs to patch for the options.
    """
    session = requests_retry_session()
    try:
        response = session.patch(ENDPOINT, json=obj)
    except (ConnectionError, MaxRetryError) as ce:
        LOGGER.error("Unable to connect to CFS: %s", ce)
        raise CFSException(ce)
    try:
        response.raise_for_status()
    except HTTPError as hpe:
        LOGGER.error("Unexptected response from CFS.")
        raise CFSException(hpe)


def hardware_sync_interval():
    key = 'hardwareSyncInterval'
    try:
        return int(read_options()[key])
    except (KeyError, ValueError, CFSException):
        LOGGER.info("Setting default check interval to 10 seconds.")
        try:
            patch_options({key: 10})
        except CFSException:
            pass
        return 10
