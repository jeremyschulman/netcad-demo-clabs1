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
# Public Imports
# -----------------------------------------------------------------------------

from netcad.device import PseudoDevice, DeviceInterface
from netcad.device.l2_interfaces import InterfaceL2Trunk
from netcad.topology import NoValidateCabling

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ..profiles.trunks import PeeringTrunk
from ..profiles.phy_port import port_ebra
from .any_device import AnyDevice
from .. import vlans

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["FloorAccessPoint"]


# -----------------------------------------------------------------------------
# Base class for all access-point devices.
# -----------------------------------------------------------------------------


class AccessPoint(AnyDevice, PseudoDevice):
    """
    The baseclass for all Access-Point devices in the design.  This device is
    designated a PseudoDevice since the containerlabs system will not be
    provisioned wih an access-point device.

    Notes
    -----
    A pseudo-device is used for design purposes so that design elements and
    their relationship can be used; but the device does not exist and therefore
    the `netcad/netcam` tools will not attempt to "do anything" to them.
    """

    device_base_name = "ap"
    sort_key = (2, 0)
    product_model = "MR84"
    os_name = "meraki"

    def build_uplink(self, dev_iface: DeviceInterface):
        """
        This function creates the cabling relationship between the AP.wired0
        interface and the provide device-interface.  The device-interface will
        also be set to use the InterfaceL2 peering trunk profile so that any
        VLANs defined on the AP will be automatically designed into the device.

        For the purpose of this containerlab demo, the AP does not really exist,
        and therefore we do not want to perform a cabling-LLDP check.  Therefore
        we will mark the wired0 interface to prevent the check by the connected
        device.

        Parameters
        ----------
        dev_iface: DeviceInterface
            The device interface where the AP will be attached.
        """
        dev = dev_iface.device
        iface_w0 = self.interfaces["wired0"]
        cable_id = f"uplink_{self.name}_{dev.name}"
        dev_iface.cable_id = cable_id
        dev_iface.profile = PeeringTrunk()
        iface_w0.cable_id = cable_id

        # mark the interface so that the connecting device does not attempt to
        # perform a cable neighbor LLDP check.

        iface_w0.cable_port_id = NoValidateCabling


# -----------------------------------------------------------------------------
# Standard "Floor" access point will have VLANs for Visitor and Employees
# -----------------------------------------------------------------------------


class FloorAccessPoint(AccessPoint):
    """
    Define an access-point to represent a 'standard access point' used in the
    building-floor design.  These access points will host two SSIDs, one for
    Employee use, and another for Visitor use.
    """

    pass


class FloorAPTrunkPort(InterfaceL2Trunk):
    """
    Define the AP wired interface trunk port type so that the desired VLANs are
    defined.

    Notes
    -----
    The purpose of this is to allow the Designer to use the AP device as the
    "source of truth" for VLANs that need to be on the trunk port on the
    connected device.  There are no APs in the actual demonstration
    containerlab; nor are there any SSIDs ;-)
    """

    port_profile = port_ebra
    native_vlan = vlans.vlan_native
    vlans = [vlans.vlan_wifi_employee, vlans.vlan_wifi_visitor]


FloorAccessPoint.interfaces["wired0"].profile = FloorAPTrunkPort()
