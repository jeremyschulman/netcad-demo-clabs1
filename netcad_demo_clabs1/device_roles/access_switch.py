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
    """
    Define the baseclass for all access-switch devices.  The general purpose of
    the access switch will to cable interfaces Ethernet7 and Ethernet8 to a
    core-switch. See the `build_uplink_to_core` for details.
    """

    UPLINK_PORTS = ["Ethernet7", "Ethernet8"]

    sort_key = (1, 0)
    device_base_name = "acc"
    template = Path("access_switch.jinja2")

    def build_uplink_to_core(self, core: CoreSwitch):
        """
        This method is used to declare the cabling between this access switch
        and the designated core switch.  The access switch will always use eth7
        and eth8.  The designated core swtich interfaces are calculated baased
        on the access-switch "device Id".  The first access switch (dev_id=1)
        will use the first two ports on the core switch, the second access
        switch (dev_id=2) will use the next two (eth3, eth4), and so on.

        Notes
        -----
        The design use of an 8-port core swtich allows for at most 4 access
        switches.  There is no enforcement of this fact in the design.  TODO:
        add such enforcement.

        Parameters
        ----------
        core: AnyContainerEosDevice
            The core switch where this access switch will be connected.

        """
        if_defs = self.interfaces

        # there are two uplink interfaces from the access device to the core
        # device. calculate the starting interface number based on the access
        # switch dev-id value.

        core_intf_baseport_id = (self.dev_id - 1) * 2 + 1
        core_if_defs = core.interfaces

        # dynamically build the cabling-id value based on the core and with
        # dev-id values.

        base_cable_id = f"uplink_{self.name}_{core.name}"
        up1_intfname, up2_intfname = self.UPLINK_PORTS

        with if_defs[up1_intfname] as up1, if_defs[up2_intfname] as up2:

            # cable the access-swtich eth7 to the first core interface

            up1.profile = UplinkTrunk()
            up1.cable_id = base_cable_id + "_1"

            with core_if_defs[f"Ethernet{core_intf_baseport_id}"] as core_intf:
                core_intf.profile = PeeringTrunk()
                core_intf.cable_id = up1.cable_id

            # cable the access-swtich eth8 to the second core interface

            up2.profile = UplinkTrunk()
            up2.cable_id = base_cable_id + "_2"

            with core_if_defs[f"Ethernet{core_intf_baseport_id + 1}"] as uplink:
                uplink.profile = PeeringTrunk()
                uplink.cable_id = up2.cable_id
