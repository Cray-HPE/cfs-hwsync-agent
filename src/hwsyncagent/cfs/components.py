'''
Created on Feb 4, 2020

@author: jsl

Copyright 2020, Cray Inc., A Hewlett Packard Enterprise Company
'''

import logging
import json
from copy import deepcopy
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import MaxRetryError

from hwsyncagent.client import requests_retry_session
from . import ENDPOINT as BASE_ENDPOINT, CFSException


LOGGER = logging.getLogger(__name__)
ENDPOINT = "%s/%s" % (BASE_ENDPOINT, __name__.lower().split('.')[-1])
DEFAULT_BODY = {'state': {'cloneUrl': '',
                          'playbook': '',
                          'commit': ''},
                'desiredState': {'cloneUrl': '',
                                 'playbook': '',
                                 'commit': ''},
                'errorCount': 0,
                'retryPolicy': 3,
                'sessionName': '',
                'enabled': True
                }


def read_registered_component_ids():
    """
    Reads all currently defined components within CFS; returns these
    as a set of names.
    """
    session = requests_retry_session()
    try:
        response = session.get(ENDPOINT)
    except (ConnectionError, MaxRetryError) as ce:
        LOGGER.error("Unable to connect to CFS")
        raise CFSException(ce)
    try:
        response.raise_for_status()
    except HTTPError as hpe:
        LOGGER.error("Unexptected response from CFS: %s", response)
        raise CFSException(hpe)
    try:
        all_components = json.loads(response.text)
    except json.JSONDecodeError as jde:
        LOGGER.error("Non-JSON response from CFS: %s", response.text)
        raise CFSException(jde)
    return set(component['id'] for component in all_components)


def create_new_component(component_id, session=None):
    """
    Creates one o CFS component representation in CFS. In most cases, 
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

    ids is an interable collection of component names to create in CFS.
    """
    session = requests_retry_session()
    ids_created = set()
    put_bodies = []
    for entry in ids:
        if entry in ids_created:
            LOGGER.warning("Request to put same ID within same PUT operation; skipping")
            continue
        new_body = deepcopy(DEFAULT_BODY)
        new_body['id'] = entry
        put_bodies.append(new_body)
        ids_created.add(entry)
    try:
        response = session.put(ENDPOINT, json=put_bodies)
    except (ConnectionError, MaxRetryError) as ce:
        LOGGER.error("Unable to connect to CFS")
        raise CFSException(ce)
    try:
        response.raise_for_status()
    except HTTPError as hpe:
        LOGGER.error("Non-zero response from CFS: %s", (response))
        raise CFSException(hpe)
