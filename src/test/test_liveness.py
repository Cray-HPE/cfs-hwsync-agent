# Copyright 2020, Cray Inc.
""" Test the hwsyncagent/liveness package """

import os
import unittest
import tempfile
from datetime import datetime, timedelta
from mock import patch

from hwsyncagent.liveness.timestamp import Timestamp


class TestSetup(object):
    def __enter__(self):
        self.path = tempfile.NamedTemporaryFile().name
        return self

    def __exit__(self, type, value, traceback):
        try:
            os.remove(self.path)
        except OSError:
            pass


def test_age():
    with TestSetup() as ts:
        t = Timestamp(path=ts.path)
        # Tests taht a non-zero amoutn of time has elapsed
        assert t.age > timedelta(seconds=0)


def test_dead():
    with TestSetup() as ts:
        t = Timestamp(path=ts.path)
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        with open(ts.path, 'w') as tstamp_file:
            tstamp_file.write(str(one_minute_ago.timestamp()))
        assert not t.alive
