This is the CFS Hardware Synchronization Agent.

The soul responsibility of this deployment is to automatically inform CFS of any changes in hardware on the system.
The agent polls both CFS and HMS and reconciles the difference so that CFS Batcher is able to schedule configuration
changes to the system.