# This is the hardware state manager client; this module concerns itself
# with interacting with the hardware state manager in order to discover
# the functional set of nodes that HSM has discovered.
# Copyright 2020, Cray Inc., A Hewlett Packard Enterprise Company


from hwsyncagent import HWSyncAgentException
from hwsyncagent import PROTOCOL

API_VERSION = 'v1'
ENDPOINT = "%s://cray-smd/hsm/%s" % (PROTOCOL, API_VERSION)


class HWStateManagerException(HWSyncAgentException):
    """
    All exceptions involving the hardware state manager should
    use this as a base class.
    """
