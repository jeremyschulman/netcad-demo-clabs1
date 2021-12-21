from pathlib import Path

from netcad.design_services import Design
from netcad.topology import TopologyDesignService
from netcad.device.l3_interfaces import InterfaceVlan
from netcad.vlan.vlan_design_service import (
    VlansDesignService,
    DeviceVlanDesignServiceLike,
)
from netcad.vlan import VlanProfileLike

from .device_roles import CoreSwitch, Acc01Switch, Acc02Switch
from .ipam import create_site_ipam, IPAM


def create_design(design: Design) -> Design:

    ipam = create_site_ipam(design)

    core = CoreSwitch(name="core01")
    sw1 = Acc01Switch(name="acc01")
    sw2 = Acc02Switch(name="acc02")

    all_devs = [core, sw1, sw2]

    design.add_devices(*all_devs).add_services(
        TopologyDesignService(topology_name=design.name, devices=all_devs),
        VlansDesignService(devices=all_devs),
    ).update()

    create_vlan_interfaces(core, ipam)
    design.update()

    return design


def create_vlan_interfaces(device: CoreSwitch, ipam: IPAM):

    vlan_svc: DeviceVlanDesignServiceLike = device.services["vlans"]

    # obtain the list of all vlans used by this device in the design

    dev_vlans = vlan_svc.all_vlans()

    #
    subnets_used = [
        (vlan, subnet) for vlan, subnet in ipam.items() if vlan in dev_vlans
    ]

    vlan: VlanProfileLike
    for vlan, subnet in subnets_used:
        with device.interfaces[f"Vlan{vlan.vlan_id}"] as iface:
            if_ipaddr = subnet.interface(name=iface, offset_octet=1)
            iface.desc = vlan.name
            iface.profile = InterfaceVlan(
                vlan=vlan, template=Path("interface_vlan.jinja2")
            )
            iface.profile.if_ipaddr = if_ipaddr
