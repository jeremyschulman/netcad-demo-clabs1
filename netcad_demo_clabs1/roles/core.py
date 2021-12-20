from netcad.device import Device

from netcad_demo_clabs1.profiles.trunks import CorePeeringTrunk
from netcad_demo_clabs1.cabling import DemoCabling


class CoreSwitch(Device):
    product_model = "cEOS-8"


# -----------------------------------------------------------------------------
#                    Standard Interface Usage
# -----------------------------------------------------------------------------

if_defs = CoreSwitch.interfaces


with if_defs["Ethernet5"] as eth5:
    eth5.profile = CorePeeringTrunk()
    eth5.cable_id = DemoCabling.uplink_core01_acc01_1


with if_defs["Ethernet6"] as eth6:
    eth6.profile = CorePeeringTrunk()
    eth6.cable_id = DemoCabling.uplink_core01_acc01_2


with if_defs["Ethernet7"] as eth7:
    eth7.profile = CorePeeringTrunk()
    eth7.cable_id = DemoCabling.uplink_core01_acc02_1


with if_defs["Ethernet8"] as eth8:
    eth8.profile = CorePeeringTrunk()
    eth8.cable_id = DemoCabling.uplink_core01_acc02_2
