#
# MIT License
#
# (C) Copyright 2019, 2021-2022 Hewlett Packard Enterprise Development LP
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
# setup.py for cfs-hwsync-agent

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("gitInfo.txt", "r") as fh:
    long_description += '\n' + fh.read()

with open(".version", "r") as fh:
    version_str = fh.read()

setuptools.setup(
    name="cfs-hwsync-agent",
    version=version_str,
    author="Cray Inc.",
    author_email="sps@cray.com",
    description="CFS Hardware Syncrhonization Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cray-HPE/cfs-hwsync-agent",
    packages=['hwsyncagent', 'hwsyncagent.cfs', 'hwsyncagent.hwstatemgr'],
    keywords="cray hpe configuration hardware sychronization agent",
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ),
)
