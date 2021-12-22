# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ..cabling import DemoCabling
from ..profiles.trunks import AccToCoreUplink
from ..profiles import access
from ..profiles.clab_ma0 import ClabAutoManagement
from .access import AccessSwitch


# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["Acc01Switch"]

# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


class Acc01Switch(AccessSwitch):
    sort_key = (1, 1)


if_defs = Acc01Switch.interfaces

# -----------------------------------------------------------------------------
#                        Host facing ports
# -----------------------------------------------------------------------------

if_defs["Management0"].profile = ClabAutoManagement()

if_defs["Ethernet1"].profile = access.Printer(desc="HR-printer")
if_defs["Ethernet2"].profile = access.Phone(desc="Bob H. phone")
if_defs["Ethernet3"].profile = access.Phone(desc="Alice C. phone")

# -----------------------------------------------------------------------------
#                        Uplink ports to core switch
# -----------------------------------------------------------------------------

with if_defs["Ethernet7"] as eth7, if_defs["Ethernet8"] as eth8:
    eth7.profile = AccToCoreUplink()
    eth7.cable_id = DemoCabling.uplink_core01_acc01_1

    eth8.profile = AccToCoreUplink()
    eth8.cable_id = DemoCabling.uplink_core01_acc01_2
