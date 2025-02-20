# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.13.0] - 2025-02-13
### Dependencies
- Bump `certifi` version to resolve CVE: https://snyk.io/vuln/SNYK-PYTHON-CERTIFI-5805047
- CASMCMS-9282: Bump Alpine version from 3.15 to 3.21, because 3.15 no longer receives security patches;
  Use Python venv inside Docker image.

## [1.12.4] - 2024-11-06
### Fixed
- CASMCMS-9190: Discard SMD components whose ID fields are blank

## [1.12.3] - 2024-09-05
### Dependencies
- CASMCMS-9135: Bump minimum `cray-services` base chart version from 10.0.5 to 11.0.0

## [1.12.2] - 2024-08-27
### Added
- Created `MANIFEST.in` file for Python package, to ensure source module is usable
- Added `install_requires` data to `setup.py`

### Changed
- List installed Python packages in Dockerfile for build logging purposes

### Dependencies
- CSM 1.6 moved to Kubernetes 1.24, so use client v24.x to ensure compatability
- Simplify how `liveness` module major/minor version are pinned
- Use `requests_retry_session` Python package instead of duplicating its code

## [1.12.1] - 2024-06-28
### Changed
- When building unstable charts, have them point to the corresponding unstable Docker image
- Remove Randy Kleinman from the chart maintainer list; add Mitch Harding

### Dependencies
- CASMCMS-9030: Bump minimum `cray-services` base chart version from 7.0.0 to 10.0.5

## [1.12.0] - 2024-02-22
### Dependencies
- Bump `kubernetes` from 12.0.1 to 22.6.0 to match CSM 1.6 Kubernetes version

## [1.11.0] - 2023-09-29
### Changed
- Parameterized HSM component discovery to filter to both Nodes and VirtualNodes during discovery.

### Fixed
- Added top level exception handling

## [1.10.0] - 2023-08-18
### Changed
- Disabled concurrent Jenkins builds on same branch/commit
- Added build timeout to avoid hung builds
- Updated to the v3 CFS api

## [1.9.2] - 2023-07-25
### Dependencies
- Use `update_external_versions` to get latest patch version of `liveness` Python module.
- Bumped dependency patch versions:
| Package                  | From     | To       |
|--------------------------|----------|----------|
| `cachetools`             | 4.2.1    | 4.2.4    |
| `msgpack`                | 1.0.2    | 1.0.5    |
| `oauthlib`               | 3.1.0    | 3.1.1    |
| `python-dateutil`        | 2.8.1    | 2.8.2    |
| `requests-oauthlib`      | 1.3.0    | 1.3.1    |
| `rsa`                    | 4.7      | 4.7.2    |
| `urllib3`                | 1.26.2   | 1.26.16  |

## [1.9.1] - 2023-07-18
### Dependencies
- Bump `PyYAML` from 5.4.1 to 6.0.1 to avoid build issue caused by https://github.com/yaml/pyyaml/issues/601

### Removed
- Removed defunct files leftover from previous versioning system

## [1.9.0] - 2023-01-12
### Changed
- Spelling corrections.
- The logging level is now controlled by a CFS option

## [1.8.2] - 2022-12-20
### Added
- Add Artifactory authentication to Jenkinsfile

## [1.8.1] 2022-12-02
### Aded
- Authenticate to CSM's artifactory

### Changed
- Convert to gitflow/gitversion.



