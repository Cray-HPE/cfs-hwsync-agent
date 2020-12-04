# Copyright 2020 Hewlett Packard Enterprise Development LP

from hwsyncagent import PROTOCOL, HWSyncAgentException

API_VERSION = 'v2'
SERVICE_NAME = 'cray-cfs-api'
ENDPOINT = "%s://%s/%s" % (PROTOCOL, SERVICE_NAME, API_VERSION)


class CFSException(HWSyncAgentException):
    """
    A base class of exceptions that occur as a result of interacting
    with CFS. All custom CFS interactions should raise this base class.
    """
