# Copyright 2020, Cray Inc., A Hewlett Packard Enterprise Company

from hwsyncagent import PROTOCOL, HWSyncAgentException

API_VERSION = 'v1'
SERVICE_NAME = 'cray-cfs-api'
ENDPOINT = "%s://%s/apis/cfs" % (PROTOCOL, SERVICE_NAME)


class CFSException(HWSyncAgentException):
    """
    A base class of exceptions that occur as a result of interacting
    with CFS. All custom CFS interactions should raise this base class.
    """
