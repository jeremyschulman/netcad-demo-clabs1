from pathlib import Path

from netcad.device import Device
from netcad.design_services import Design
from netcad.topology import TopologyDesignService
from netcad.device.l3_interfaces import InterfaceVlan
from netcad.vlan.vlan_design_service import (
    VlansDesignService,
    DeviceVlanDesignServiceLike,
)
from netcad.vlan import VlanProfileLike

from .profiles.clab_ma0 import Management0
from .device_roles import CoreSwitch, Acc01Switch, Acc02Switch
from .ipam import create_site_ipam, IPAM


def create_design(design: Design) -> Design:

    ipam = create_site_ipam(design)

    core = CoreSwitch(name="core01.d")
    sw1 = Acc01Switch(name="acc01.d")
    sw2 = Acc02Switch(name="acc02.d")

    all_devs = [core, sw1, sw2]

    design.add_devices(*all_devs).add_services(
        TopologyDesignService(topology_name=design.name, devices=all_devs),
        VlansDesignService(devices=all_devs),
    ).update()

    set_mgmt_ipaddr(core, ipam, 2)
    set_mgmt_ipaddr(sw1, ipam, 3)
    set_mgmt_ipaddr(sw2, ipam, 4)

    create_vlan_interfaces(core, ipam, host_offset=1)

    design.update()

    return design


def set_mgmt_ipaddr(device: Device, ipam: IPAM, host_offset: int):

    oob_subnet = ipam["OOB"]

    with device.interfaces["Management0"] as ma0:
        ma0_if_ipaddr = oob_subnet.interface(name=ma0, offset_octet=host_offset)
        ma0.profile = Management0(
            if_ipaddr=oob_subnet.interface(name=ma0, offset_octet=host_offset)
        )
        device.primary_ip = ma0_if_ipaddr.ip


def create_vlan_interfaces(device: CoreSwitch, ipam: IPAM, host_offset: int):

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
            if_ipaddr = subnet.interface(name=iface, offset_octet=host_offset)
            iface.desc = vlan.name
            iface.profile = InterfaceVlan(
                vlan=vlan, template=Path("interface_vlan.jinja2")
            )
            iface.profile.if_ipaddr = if_ipaddr
