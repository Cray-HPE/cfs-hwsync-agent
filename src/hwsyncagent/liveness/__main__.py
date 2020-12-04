#!/usr/bin/env python
# Copyright 2020, Cray Inc.
'''
This entrypoint is used to determine if this service is still active/alive
from a kubernetes liveness probe perspective.

This service is deemed to be 'alive' and healthy if the
main loop has executed relatively recently. The period of time for how frequently
the agent checks for operational work is defined as a function of event frequency from
kubernetes, so this liveness probe needs a larger than normal window to account for
periods of time without a recent liveness cycle.

Created on April 28, 2020

@author: jsl
'''

import sys
import logging
import os

from hwsyncagent.liveness import TIMESTAMP_PATH
from .timestamp import Timestamp


LOGGER = logging.getLogger('hwsyncagent.liveness.main')
DEFAULT_LOG_LEVEL = logging.INFO


def setup_logging():
    log_format = "%(asctime)-15s - %(levelname)-7s - %(name)s - %(message)s"
    requested_log_level = os.environ.get('LOG_LEVEL', DEFAULT_LOG_LEVEL)
    log_level = logging.getLevelName(requested_log_level)
    logging.basicConfig(level=log_level, format=log_format)


if __name__ == '__main__':
    setup_logging()
    timestamp = Timestamp.byref(TIMESTAMP_PATH)
    if timestamp.alive:
        LOGGER.info("%s is considered valid; the application is alive!", timestamp)
        sys.exit(0)
    else:
        LOGGER.warning("Timestamp is no longer considered valid.")
        sys.exit(1)
