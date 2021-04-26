# Copyright 2020-2021 Hewlett Packard Enterprise Development LP
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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# (MIT License)

'''
The CFS API contains options that are pertinent to how the HWSync Agent
should operate. This module allows us to read those options from the API.
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
