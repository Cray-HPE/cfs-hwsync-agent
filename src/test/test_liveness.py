#
# MIT License
#
# (C) Copyright 2020-2022 Hewlett Packard Enterprise Development LP
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
