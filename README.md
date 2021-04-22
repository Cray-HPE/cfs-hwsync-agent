This is the CFS Hardware Synchronization Agent.

The sole responsibility of this deployment is to automatically inform CFS of any changes in hardware on the system.
The agent polls both CFS and HMS and reconciles the difference so that CFS Batcher is able to schedule configuration
changes to the system.

## Versioning
Use [SemVer](http://semver.org/). The version is located in the [.version](.version) file. Other files have this
version string written to them at build time using the [update_versions.sh](update_versions.sh) script, based
on the information in the [update_versions.conf](update_versions.conf) file.
