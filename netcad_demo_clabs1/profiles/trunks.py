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
# This file contains the Interface Profiles for "trunk" ports used in the
# designs.
# =============================================================================

# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from pathlib import Path

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from netcad.vlans import InterfaceL2Trunk, VlansFromPeer, VlansAll
from netcad.device import PeerInterfaceId

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from netcad_demo_clabs1.vlans import vlan_native
from netcad_demo_clabs1.profiles.phy_port import port_ebra

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["PeeringTrunk", "UplinkTrunk"]

# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------


class PeeringTrunk(InterfaceL2Trunk):
    """
    Used by core switches, automatically uses the same VLANs as defined on the
    connected access switches.
    """

    port_profile = port_ebra
    desc = PeerInterfaceId()
    native_vlan = VlansFromPeer()
    vlans = VlansFromPeer()
    template = Path("interface_trunk.jinja2")


class UplinkTrunk(InterfaceL2Trunk):
    """
    Used by access switches, automatically uses all VLANs that are defined on
    the local interface ports.
    """

    port_profile = port_ebra
    desc = PeerInterfaceId()
    native_vlan = vlan_native
    vlans = VlansAll()
    template = Path("interface_trunk.jinja2")
