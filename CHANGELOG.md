# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- When building unstable charts, have them point to the corresponding unstable Docker image
- Remove Randy Kleinman from the chart maintainer list; add Mitch Harding

## [1.8.3] - 2023-09-28
### Fixed
- Added top level exception handling

### Changed
- Disabled concurrent Jenkins builds on same branch/commit
- Added build timeout to avoid hung builds

### Dependencies
- Bump `PyYAML` from 5.4.1 to 6.0.1 to avoid build issue caused by https://github.com/yaml/pyyaml/issues/601

### Removed
- Removed defunct files leftover from previous versioning system

## [1.8.2] - 2022-12-20
### Added
- Add Artifactory authentication to Jenkinsfile

## [1.8.1] 2022-12-02
### Aded
- Authenticate to CSM's artifactory

### Changed
- Convert to gitflow/gitversion.
