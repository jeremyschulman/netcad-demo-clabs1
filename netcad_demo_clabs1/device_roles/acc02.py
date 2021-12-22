# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ..cabling import DemoCabling
from ..profiles.trunks import AccToCoreUplink
from .access import AccessSwitch

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["Acc02Switch"]


class Acc02Switch(AccessSwitch):
    sort_key = (1, 2)


if_defs = Acc02Switch.interfaces

# -----------------------------------------------------------------------------
#                        Uplink ports to core switch
# -----------------------------------------------------------------------------

with if_defs["Ethernet7"] as eth7, if_defs["Ethernet8"] as eth8:
    eth7.profile = AccToCoreUplink()
    eth7.cable_id = DemoCabling.uplink_core01_acc02_1

    eth8.profile = AccToCoreUplink()
    eth8.cable_id = DemoCabling.uplink_core01_acc02_2
