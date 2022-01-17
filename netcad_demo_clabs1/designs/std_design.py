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

# =============================================================================
# This file contains the "standard floor design" aspects.  Each building-floor
# will be designed with the following:
#
#   * one core switch
#   * two access swiches
#   * one access-point
#
# Each access switch will be connected via two ethernet ports to the core. The
# access-point will be connected to the first access switch.  For specific
# cabling design, refer to the `device_roles` module for each.
#
# =============================================================================


# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from pathlib import Path
from itertools import islice
from ipaddress import IPv4Interface, IPv4Network

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from netcad.design import Design
from netcad.topology import TopologyDesignService

from netcad.vlans import (
    InterfaceVlan,
    VlansDesignService,
    DeviceVlanDesignServiceLike,
    VlanProfileLike,
)

from netcad.ipam import IPAM

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ..profiles.clab_ma0 import Management0
from ..device_roles import CoreSwitch, AccessSwitch, AnyDevice, FloorAccessPoint
from ..ipam import create_site_ipam

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["create_std_design", "set_vlan_interfaces"]


# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------


def create_std_design(design: Design):
    """
    Create the standard building-floor design pattern.

    Parameters
    ----------
    design: Design
        The design instance that will be build
    """

    # The building and floor ID values are taken from the `netcad.toml`
    # configuration file.

    bld_id, flr_id = design.config["building"], design.config["floor"]

    # create the IP Address Management instance that stores all of the subnets
    # used in the design.

    ipam = create_site_ipam(design)

    # create the standard set of four devices per building-floor

    core = CoreSwitch(dev_id=1, bld_id=bld_id, flr_id=flr_id)
    sw1 = AccessSwitch(dev_id=1, bld_id=bld_id, flr_id=flr_id)
    sw2 = AccessSwitch(dev_id=2, bld_id=bld_id, flr_id=flr_id)
    ap1 = FloorAccessPoint(dev_id=1, bld_id=bld_id, flr_id=flr_id)

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

    net_id = design.config["net_id"]
    mgmt_subnet = get_mgmt_subnet(net_id=net_id, ipam=ipam)

    # Note the .1 is assigned to the containerlab system host interface

    set_mgmt_ipaddr(core, mgmt_subnet, host_offset=2)
    set_mgmt_ipaddr(sw1, mgmt_subnet, host_offset=3)
    set_mgmt_ipaddr(sw2, mgmt_subnet, host_offset=4)

    set_vlan_interfaces(design)

    design.update()


def set_vlan_interfaces(design: Design):
    """
    Assgin IP addresses to the SVIs on devices that need them.
    """
    ipam = design.ipams[0]
    dev_nn = design.config["nicknames"]

    create_vlan_interfaces(dev_nn["core01"], ipam=ipam, host_offset=1)


def get_mgmt_subnet(net_id: int, ipam: IPAM) -> IPv4Network:
    """
    This function is used to determine the management subnet for this design.
    The OOB network is carved up into /28 chunks per "network ID"; i.e each
    building-floor has a designated network ID value, and that value determines
    which /28 chunk to use.  This approach allows us to use the single
    containerlab / docker network that is a /24.

    Parameters
    ----------
    net_id: int
        The network ID value as defined in the `netcad.toml` configuration file
        for this specific design network.

    ipam: IPAM
        The IPAM instance that stores the overall OOB network instance.

    Returns
    -------
    IPv4Network
        The network instance that will be used as the base network for assigning
        the Management0 interface IP addresss.
    """

    oob_subnet = ipam["OOB"]

    # chunk the OOB network into /28 subnets and then use the design 'net_id'
    # value to select the specific subnet to use for this design.  So if
    # net_id=1 then this desgin will get the first /28, if net_id=2 it will get
    # the second /28, etc.

    oob_pf28s = oob_subnet.ip_network.subnets(new_prefix=28)
    design_p28 = next(islice(oob_pf28s, net_id - 1, None))
    return design_p28


def set_mgmt_ipaddr(device: AnyDevice, mgmt_subnet: IPv4Network, host_offset: int):
    """
    This function defines the Management0 interface on the device.  The IP
    address is the mgmt-subnet base network address + the host-offset.  The
    Management0 is set to use a /24 prefix, artifically, so that it will conform
    to the use of the docker-network that is a /24 for all host manaegment.

    Parameters
    ----------
    device: AnyDevice
        The device that is begin assigned its Management0

    mgmt_subnet: IPv4Network
        The IPv4 network instance for this network design management subnet.

    host_offset: int
        The device IP offset value that is added to the subnet base to compute
        the specific IP interface address.
    """

    host_ip = mgmt_subnet.network_address + host_offset

    with device.interfaces["Management0"] as ma0:
        ma0_if_ipaddr = IPv4Interface((host_ip, 24))
        ma0.profile = Management0(if_ipaddr=ma0_if_ipaddr)
        device.primary_ip = ma0_if_ipaddr.ip


def create_vlan_interfaces(device: AnyDevice, ipam: IPAM, host_offset: int):
    """
    This function is used to create Vlan Interfaces for each VLAN defined on the
    device.  For example, if a device has 4 VLANs defined, and those VLANs have assocaited
    IPAM networks, then this function will create SVIs for each of those four VLANs.

    Parameters
    ----------
    device: AnyDevice
        The device that is being designed.

    ipam: IPAM
        The IPAM instance that holds all of the subnets defined in the design.
        Some of these will have "names" that are VlanProfile instances.  Each of
        these is then used to design in the SVI interface.

    host_offset: int
        This value is used to add to the base of each of the VLAN associated
        networks to compute the device specific SVI interface IP address.

    """

    vlan_svc: DeviceVlanDesignServiceLike = device.services["vlans"]

    # obtain the list of all vlans used by this device in the design

    dev_vlans = vlan_svc.all_vlans()

    # find all of the IPAM subnets that are VLAN associated, and whose VLANs are
    # begin used on this device.

    subnets_used = [
        (vlan, subnet) for vlan, subnet in ipam.items() if vlan in dev_vlans
    ]

    # for each VLAN subnet that should be on this device create a "Vlan<n>"
    # interface and calcualte+assign the IP interface address.

    vlan: VlanProfileLike
    for vlan, subnet in subnets_used:
        with device.interfaces[f"Vlan{vlan.vlan_id}"] as iface:
            if_ipaddr = subnet.interface(name=iface, offset_octet=host_offset)
            iface.desc = vlan.name
            iface.profile = InterfaceVlan(
                vlan=vlan, template=Path("interface_vlan.jinja2")
            )
            iface.profile.if_ipaddr = if_ipaddr
