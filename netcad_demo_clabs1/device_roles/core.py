# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from pathlib import Path

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from netcad_demo_clabs1.profiles.trunks import CorePeeringTrunk
from netcad_demo_clabs1.cabling import DemoCabling

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .any_device import AnyDevice


class CoreSwitch(AnyDevice):
    sort_key = (0, 0)
    template = Path("core_switch.jinja2")


# -----------------------------------------------------------------------------
#                    Standard Interface Usage
# -----------------------------------------------------------------------------

if_defs = CoreSwitch.interfaces


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
