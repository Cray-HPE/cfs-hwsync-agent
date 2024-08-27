# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- When building unstable charts, have them point to the corresponding unstable Docker image
- Remove Randy Kleinman from the chart maintainer list; add Mitch Harding
- List installed Python packages in Dockerfile for build logging purposes

### Dependencies
- Simplify how `liveness` module major/minor version are pinned

## [1.9.3] - 2023-09-28
### Fixed
- Added top level exception handling

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



