from pathlib import Path

from netcad.device.l2_interfaces import InterfaceL2Access

from netcad_demo_clabs1.vlans import vlan_printers, vlan_phones
from netcad_demo_clabs1.profiles.phy_port import port_ebra


class Printer(InterfaceL2Access):
    port_profile = port_ebra
    vlan = vlan_printers
    template = Path("interface_access.jinja2")


class Phone(InterfaceL2Access):
    port_profile = port_ebra
    vlan = vlan_phones
    template = Path("interface_access.jinja2")
