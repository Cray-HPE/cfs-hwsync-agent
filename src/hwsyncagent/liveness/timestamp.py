# Copyright 2020, Cray Inc.
'''
A set of routines for creating or reading from an existing timestamp file.
Created on April 27, 2020

@author: jsl
'''
import logging
from datetime import datetime, timedelta

from hwsyncagent.liveness import TIMESTAMP_PATH
from hwsyncagent.cfs.options import hardware_sync_interval
from liveness.timestamp import Timestamp as TimestampBase


LOGGER = logging.getLogger(__name__)


class Timestamp(TimestampBase):

    @property
    def max_age(self):
        """
        The maximum amount of time that can elapse before we consider the timestamp
        as invalid. This max_age is defined by the period of time between required
        checks to HSM, which is defined by the set of options contained in the API.

        This value is returned as a timedelta object.
        """
        interval = 20 + hardware_sync_interval()
        computation_time = timedelta(seconds=interval)
        return computation_time
