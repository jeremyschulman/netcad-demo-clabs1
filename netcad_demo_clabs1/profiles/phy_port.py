from netcad.phy_port import (
    PhyPortProfile,
    PortCable,
    CableMediaType,
    CableTerminationType,
)


port_ebra = PhyPortProfile(
    name="EbraTestPhyPort",
    cabling=PortCable(
        media=CableMediaType.virtual, termination=CableTerminationType.virtual
    ),
    transceiver=None,
)
