#
# MIT License
#
# (C) Copyright 2019-2022, 2024-2025 Hewlett Packard Enterprise Development LP
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
# Base image
FROM artifactory.algol60.net/docker.io/alpine:3.21 AS base
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
COPY constraints.txt requirements.txt ./
RUN apk add --upgrade --no-cache apk-tools &&  \
	apk update && \
	apk add --no-cache gcc g++ python3 python3-dev musl-dev libffi-dev openssl-dev py3-pip && \
	apk -U upgrade --no-cache && \
    python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    pip3 list --format freeze && \
    pip3 install --no-cache-dir -U pip -c constraints.txt && \
    pip3 list --format freeze && \
    pip3 install --no-cache-dir --disable-pip-version-check -U setuptools wheel -c constraints.txt && \
    pip3 list --format freeze && \
    pip3 install --no-cache-dir --disable-pip-version-check -r requirements.txt && \
    pip3 list --format freeze
COPY src/hwsyncagent/ lib/hwsyncagent/

# Testing Image
FROM base AS testing
WORKDIR /app/
COPY src/test lib/test/
COPY docker_test_entry.sh .
COPY test-requirements.txt .
RUN pip3 install --no-cache-dir --disable-pip-version-check -r test-requirements.txt && \
    pip3 list --format freeze
CMD [ "./docker_test_entry.sh" ]

# Codestyle reporting
FROM testing AS codestyle
WORKDIR /app/
COPY docker_codestyle_entry.sh setup.cfg ./
CMD [ "./docker_codestyle_entry.sh" ]

# Application Image
FROM base AS application
USER 65534:65534
ENV PYTHONPATH "/app/lib/"
ENTRYPOINT [ "python3", "-m", "hwsyncagent" ]
