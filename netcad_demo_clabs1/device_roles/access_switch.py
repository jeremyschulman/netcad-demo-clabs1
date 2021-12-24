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

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ..profiles.trunks import UplinkTrunk, PeeringTrunk
from .any_device import AnyContainerEosDevice
from .core_switch import CoreSwitch


class AccessSwitch(AnyContainerEosDevice):
    sort_key = (1, 0)
    device_base_name = "acc"
    template = Path("access_switch.jinja2")

    def build_uplink_to_core(self, core: CoreSwitch):
        if_defs = self.interfaces

        # there are two uplink interfaces from the access device to the core
        # device. calculate the starting interface number based on the access
        # switch dev-id value.

        core_intf_baseport_id = (self.dev_id - 1) * 2 + 1
        core_if_defs = core.interfaces

        # dynamically build the cabling-id value based on the core and with
        # dev-id values.

        base_cable_id = f"uplink_{self.name}_{core.name}"

        with if_defs["Ethernet7"] as eth7, if_defs["Ethernet8"] as eth8:
            eth7.profile = UplinkTrunk()
            eth7.cable_id = base_cable_id + "_1"

            with core_if_defs[f"Ethernet{core_intf_baseport_id}"] as core_intf:
                core_intf.profile = PeeringTrunk()
                core_intf.cable_id = eth7.cable_id

            eth8.profile = UplinkTrunk()
            eth8.cable_id = base_cable_id + "_2"
            with core_if_defs[f"Ethernet{core_intf_baseport_id + 1}"] as uplink:
                uplink.profile = PeeringTrunk()
                uplink.cable_id = eth8.cable_id
