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

from netcad.device import PseudoDevice, DeviceInterface
from netcad.device.l2_interfaces import InterfaceL2Trunk

from ..profiles.trunks import PeeringTrunk
from ..profiles.phy_port import port_ebra
from .any_device import AnyDevice
from .. import vlans

__all__ = ["FloorAccessPoint"]


# -----------------------------------------------------------------------------
# Base class for all access-point devices.
# -----------------------------------------------------------------------------


class AccessPoint(AnyDevice, PseudoDevice):
    device_base_name = "ap"
    sort_key = (2, 0)
    product_model = "MR84"
    os_name = "meraki"

    def build_uplink(self, dev_iface: DeviceInterface):
        dev: AnyDevice = dev_iface.device
        iface_w0 = self.interfaces["wired0"]
        cable_id = f"uplink_{self.name}_{dev.name}"
        dev_iface.cable_id = cable_id
        dev_iface.profile = PeeringTrunk()
        iface_w0.cable_id = cable_id


# -----------------------------------------------------------------------------
# Standard "Floor" access point will have VLANs for Visitor and Employees
# -----------------------------------------------------------------------------


class FloorAccessPoint(AccessPoint):
    pass


class FloorAPTrunkPort(InterfaceL2Trunk):
    port_profile = port_ebra
    native_vlan = vlans.vlan_native
    vlans = [vlans.vlan_wifi_employee, vlans.vlan_wifi_visitor]


FloorAccessPoint.interfaces["wired0"].profile = FloorAPTrunkPort()
