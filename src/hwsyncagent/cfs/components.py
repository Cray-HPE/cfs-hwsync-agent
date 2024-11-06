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
import logging
import json
from copy import deepcopy
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

from hwsyncagent.client import requests_retry_session
from . import ENDPOINT as BASE_ENDPOINT, CFSException


LOGGER = logging.getLogger(__name__)
ENDPOINT = "%s/%s" % (BASE_ENDPOINT, __name__.lower().split('.')[-1])
DEFAULT_BODY = {'state': [],
                'desired_config': '',
                'error_count': 0,
                'enabled': True
                }


def read_registered_component_ids():
    """
    Reads all currently defined components within CFS; returns these
    as a set of names.
    """
    return set(component["id"] for component in iter_components())


def iter_components(**kwargs):
    """Get information for all CFS sessions"""
    next_parameters = kwargs
    while True:
        data = get_components(parameters=next_parameters)
        for component in data["components"]:
            yield component
        next_parameters = data["next"]
        if not next_parameters:
            break


def get_components(parameters=None):
    """Get components and state information stored in CFS"""
    if not parameters:
        parameters = {}
    session = requests_retry_session()
    try:
        response = session.get(ENDPOINT, params=parameters)
    except (ConnectionError, MaxRetryError) as ce:
        LOGGER.error("Unable to connect to CFS")
        raise CFSException(ce)
    try:
        response.raise_for_status()
    except HTTPError as hpe:
        LOGGER.error("Unexpected response from CFS: %s", response)
        raise CFSException(hpe)
    try:
        components_data = json.loads(response.text)
    except json.JSONDecodeError as jde:
        LOGGER.error("Non-JSON response from CFS: %s", response.text)
        raise CFSException(jde)
    return components_data


def create_new_component(component_id, session=None):
    """
    Creates one CFS component representation in CFS. In most cases,
    component_id represents a hardware xname. This operation is an
    idempotent put action, so any subsequent calls with the same id
    or ids will functionally 'zero' a component to a newly initialized
    state.
    """
    session = session or requests_retry_session()
    new_body = deepcopy(DEFAULT_BODY)
    new_body['id'] = component_id
    try:
        response = session.put(ENDPOINT, json=[new_body])
    except (ConnectionError, MaxRetryError) as ce:
        LOGGER.error("Unable to connect to CFS")
        raise CFSException(ce)
    try:
        response.raise_for_status()
    except HTTPError as hpe:
        LOGGER.error("Non-zero response from CFS: %s", (response))
        raise CFSException(hpe)


def create_new_components(ids):
    """
    This routine supports creation of multiple components.

    ids is an iterable collection of component names to create in CFS.
    """
    session = requests_retry_session()
    put_filters = { 'ids': ','.join(list(set(ids))) }
    put_patch = deepcopy(DEFAULT_BODY)
    put_body = { 'patch': put_patch, 'filters': put_filters }
    LOGGER.info(str(put_body))
    try:
        response = session.put(ENDPOINT, json=put_body)
    except (ConnectionError, MaxRetryError) as ce:
        LOGGER.error("Unable to connect to CFS")
        raise CFSException(ce)
    if response.text:
        LOGGER.info(f"text: {response.text}")
    if response.body:
        LOGGER.info(f"text: {response.body}")
    try:
        response.raise_for_status()
    except HTTPError as hpe:
        LOGGER.error("Non-zero response from CFS: %s", (response))
        raise CFSException(hpe)
