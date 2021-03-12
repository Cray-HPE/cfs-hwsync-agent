'''
Created on Jan 29, 2020

@author: jsl
Copyright 2020-2021, Hewlett Packard Enterprise Development LP
'''

import logging
import sys
import threading
from time import sleep

from .cfs.options import hardware_sync_interval
from .cfs.components import read_registered_component_ids, create_new_components
from .cfs import CFSException
from .hwstatemgr.components import read_all_node_xnames, HWStateManagerException
from hwsyncagent.liveness.timestamp import Timestamp


LOG_LEVEL = logging.INFO
LOGGER = logging.getLogger('hwsyncagent.main')
LOGGER.setLevel(LOG_LEVEL)


def monotonic_liveliness_heartbeat():
    """
    Periodically add a timestamp to disk; this allows for reporting of basic
    health at a minimum rate. This prevents the pod being marked as dead if
    a period of no events have been monitored from k8s for an extended
    period of time.
    """
    while True:
        Timestamp()
        sleep(10)


def setup_logging():
    log_format = "%(asctime)-15s - %(levelname)-7s - %(name)s - %(message)s"
    formatter = logging.Formatter(log_format)
    _stdout_handler = logging.StreamHandler(sys.stdout)
    _stdout_handler.setLevel(LOG_LEVEL)
    _stdout_handler.setFormatter(formatter)
    PROJECT_LOGGER = logging.getLogger('hwsyncagent')
    PROJECT_LOGGER.addHandler(_stdout_handler)
    PROJECT_LOGGER.setLevel(LOG_LEVEL)
    LOGGER.info("logging established")


def main_loop():
    LOGGER.info("Entering main event loop...")

    # Create a liveness thread to indicate overall health of the pod
    heartbeat = threading.Thread(target=monotonic_liveliness_heartbeat,
                                 args=())
    heartbeat.start()

    previous_members = set()
    while True:
        # Normally, we would not sleep on our first iteration of the
        # service, but incidentally, our first iteration fails because
        # the istio proxy sidecar has not yet set up its routes correctly.
        # For this reason, logic specific to skipping the sleep on the first
        # iteration has been removed.
        LOGGER.debug("Querying sync interval for sleep")
        sleep(hardware_sync_interval())
        Timestamp()

        # Query HSM for members
        try:
            LOGGER.debug("Querying xnames from HSM")
            members = read_all_node_xnames()
        except HWStateManagerException:
            LOGGER.error("Unable to query HSM member components; retrying...")
            continue
        new_members = members - previous_members
        removed_members = previous_members - members
        if new_members:
            new_members_count = len(new_members)
            if new_members_count <= 5:
                LOGGER.info("%s discovered from HSM.", ', '.join(sorted(new_members)))
            else:
                LOGGER.info("%s discovered members from HSM.", new_members_count)
        if removed_members:
            removed_members_count = len(removed_members)
            LOGGER.info("HSM no longer reporting membership for %s components...",
                        removed_members_count)
        previous_members = members

        # Query the set of components CFS is aggregating status for
        try:
            LOGGER.debug("Querying CFS component IDs")
            cfs_defined_components = read_registered_component_ids()
        except CFSException as cfse:
            LOGGER.info(cfse)
            continue

        # Determine which components are missing from CFS
        missing_xnames_from_cfs = members - cfs_defined_components

        # Create all missing components
        if missing_xnames_from_cfs:
            try:
                LOGGER.debug("Creating missing components in CFS")
                create_new_components(sorted(missing_xnames_from_cfs))
                LOGGER.info("Registered %s new components with CFS.",
                            len(missing_xnames_from_cfs))
            except CFSException as cfse:
                LOGGER.info(cfse)
                continue


if __name__ == '__main__':
    setup_logging()
    main_loop()

