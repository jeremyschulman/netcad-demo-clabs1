# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from pathlib import Path

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ..profiles.trunks import CorePeeringTrunk
from ..profiles.clab_ma0 import ClabAutoManagement
from ..cabling import DemoCabling
from .any_device import AnyDevice


# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["CoreSwitch"]

# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


class CoreSwitch(AnyDevice):
    """
    Define the device profile for a "core" device.  These devices represent the
    aggreation of "access" devices.
    """

    sort_key = (0, 0)
    template = Path("core_switch.jinja2")


# -----------------------------------------------------------------------------
#                    Standard Interface Usage
# -----------------------------------------------------------------------------

if_defs = CoreSwitch.interfaces

if_defs["Management0"].profile = ClabAutoManagement()


with if_defs["Ethernet1"] as eth:
    eth.profile = CorePeeringTrunk()
    eth.cable_id = DemoCabling.uplink_core01_acc01_1


with if_defs["Ethernet2"] as eth:
    eth.profile = CorePeeringTrunk()
    eth.cable_id = DemoCabling.uplink_core01_acc01_2


with if_defs["Ethernet3"] as eth:
    eth.profile = CorePeeringTrunk()
    eth.cable_id = DemoCabling.uplink_core01_acc02_1


with if_defs["Ethernet4"] as eth:
    eth.profile = CorePeeringTrunk()
    eth.cable_id = DemoCabling.uplink_core01_acc02_2
