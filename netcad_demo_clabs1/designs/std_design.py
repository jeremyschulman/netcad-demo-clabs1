#  MIT License
#
#  Copyright (c) 2021 Jeremy Schulman
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from pathlib import Path
from itertools import islice
from ipaddress import IPv4Interface

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from netcad.design_services import Design
from netcad.topology import TopologyDesignService
from netcad.device.l3_interfaces import InterfaceVlan
from netcad.vlan.vlan_design_service import (
    VlansDesignService,
    DeviceVlanDesignServiceLike,
)

from netcad.vlan import VlanProfileLike

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ..profiles.clab_ma0 import Management0
from ..device_roles import CoreSwitch, AccessSwitch, AnyDevice, FloorAccessPoint
from ..ipam import create_site_ipam, IPAM

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["create_std_design"]


# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------


def create_std_design(design: Design):

    bld_id, fl_id = design.config["building"], design.config["floor"]

    ipam = create_site_ipam(design, bld_id=bld_id, flr_id=fl_id)

    core = CoreSwitch(dev_id=1, bld_id=bld_id, fl_id=fl_id)
    sw1 = AccessSwitch(dev_id=1, bld_id=bld_id, fl_id=fl_id)
    sw2 = AccessSwitch(dev_id=2, bld_id=bld_id, fl_id=fl_id)
    ap1 = FloorAccessPoint(dev_id=1, bld_id=bld_id, fl_id=fl_id)

    # save the nicknames of the devices in the design.config area so that these
    # devices can be retrieved later without having to know the explicit
    # hostname values.

    design.config["nicknames"] = dev_nicknames = dict()

    dev_nicknames["core01"] = core
    dev_nicknames["acc01"] = sw1
    dev_nicknames["acc02"] = sw2
    dev_nicknames["ap01"] = ap1

    # connect the devices together in the standard configuration; see device
    # roles for sepcific details.  Connect the AP01 device to the first access
    # switch on Ethernet1.

    sw1.build_uplink_to_core(core)
    sw2.build_uplink_to_core(core)
    ap1.build_uplink(sw1.interfaces["Ethernet1"])

    # Add the devices to the desgin services for topology and vlans.

    all_devs = [core, sw1, sw2, ap1]

    design.add_devices(*all_devs).add_services(
        TopologyDesignService(topology_name=design.name, devices=all_devs),
        VlansDesignService(devices=all_devs),
    ).update()

    # assgin IP addresses to the management interfaces

    set_mgmt_ipaddr(core, ipam, 2, net_id=design.config["net_id"])
    set_mgmt_ipaddr(sw1, ipam, 3, net_id=design.config["net_id"])
    set_mgmt_ipaddr(sw2, ipam, 4, net_id=design.config["net_id"])

    # assgin IP addresses to the SVIs on devices that need them.
    create_vlan_interfaces(core, ipam, host_offset=1)


def set_mgmt_ipaddr(device: AnyDevice, ipam: IPAM, host_offset: int, net_id: int):

    oob_subnet = ipam["OOB"]

    # chunk the OOB network into /28 subnets and then use the design 'net_id'
    # value to select the specific subnet to use for this design.  So if
    # net_id=1 then this desgin will get the first /28, if net_id=2 it will get
    # the second /28, etc.

    oob_pf28s = oob_subnet.ip_network.subnets(new_prefix=28)
    design_p28 = next(islice(oob_pf28s, net_id - 1, None))
    host_ip = design_p28.network_address + host_offset

    # the container lab needs the IP address to be a /24 unless I want to carve
    # out per topology subnets, which I don't.  So forcing the prefix length to
    # 24 so that the ipaddr checks pass.

    with device.interfaces["Management0"] as ma0:
        ma0_if_ipaddr = IPv4Interface((host_ip, 24))
        ma0.profile = Management0(if_ipaddr=ma0_if_ipaddr)
        device.primary_ip = ma0_if_ipaddr.ip


def create_vlan_interfaces(device: CoreSwitch, ipam: IPAM, host_offset: int):

    vlan_svc: DeviceVlanDesignServiceLike = device.services["vlans"]

    # obtain the list of all vlans used by this device in the design
    dev_vlans = vlan_svc.all_vlans()

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
