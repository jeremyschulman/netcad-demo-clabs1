from netcad.device import Device

from netcad_demo_clabs1.profiles.trunks import AccToCoreUplink


class AccessSwitch(Device):
    product_model = "cEOS-8"


# -----------------------------------------------------------------------------
#                    Standard Interface Usage
# -----------------------------------------------------------------------------

if_defs = AccessSwitch.interfaces


with if_defs["Ethernet7"] as eth7:
    eth7.profile = AccToCoreUplink()


with if_defs["Ethernet8"] as eth7:
    eth7.profile = AccToCoreUplink()
