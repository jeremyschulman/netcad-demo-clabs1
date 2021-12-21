from pathlib import Path

from netcad.device.l2_interfaces import InterfaceL2Trunk
from netcad.device import PeerInterfaceId
from netcad.vlan import VlansFromPeer, VlansAll


from netcad_demo_clabs1.vlans import vlan_native
from netcad_demo_clabs1.profiles.phy_port import port_ebra


class CorePeeringTrunk(InterfaceL2Trunk):
    """
    Used by core switches, automatically uses the same VLANs as defined on the
    connected access switches.
    """

    port_profile = port_ebra
    desc = PeerInterfaceId()
    native_vlan = VlansFromPeer()
    vlans = VlansFromPeer()
    template = Path("interface_trunk.jinja2")


class AccToCoreUplink(InterfaceL2Trunk):
    """
    Used by access switches, automatically uses all VLANs that are defined on
    the local interface ports.
    """

    port_profile = port_ebra
    desc = PeerInterfaceId()
    native_vlan = vlan_native
    vlans = VlansAll()
    template = Path("interface_trunk.jinja2")
