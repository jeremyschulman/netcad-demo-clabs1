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
# This file contains the IP Address Management aspects for each of the subnets
# used in the design.
# =============================================================================

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from netcad.design_services import Design
from netcad.ipam import IPAM

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from . import vlans

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["create_site_ipam"]


def create_site_ipam(design: Design) -> IPAM:
    """
    This function is responsible for creating the IP subnets used in the design.
    These subnets are associated into an IPAM instance object.  Many of the
    subnet "names" are VlanProfile objects; which allows the Designer to then
    easily create SVI interfaces based on recognizing these names are Vlans.
    Refer to the file `designs.std_design.py` for example.

    Notes
    -----
    The IPAM instance created in this function is also added into the
    design.ipams property with the name "0"; the name of 0 is arbitrary since _a
    name_ is required. We could have called this anything, such as "default".
    This choice is up to the Designer.

    Parameters
    ----------
    design: Design
        The design instance that is being creating.

    Returns
    -------
    IPAM
        The IPAM instance that was created in this function.
    """
    ipam = IPAM(name=design.name)

    # The OOB network **MUST** be whatever the containerlab system is using for
    # management bridging.  Mine happened to be the 172.20.20.0/24.  Your
    # milleage may vary, so if you are trying to use this, be aware.
    # TODO: should make this setting in the `netcad.toml` config file somehow.

    ipam.network("OOB", prefix="172.20.20.0/24")

    ipam.network(name=vlans.vlan_phones, prefix="10.10.1.0/24")
    ipam.network(name=vlans.vlan_printers, prefix="10.10.2.0/24")
    ipam.network(name=vlans.vlan_media_iptvs, prefix="10.10.3.0/24")

    ipam.network(name=vlans.vlan_wifi_employee, prefix="10.100.1.0/24")
    ipam.network(name=vlans.vlan_employee_desk, prefix="10.101.1.0/24")

    ipam.network(name=vlans.vlan_wifi_visitor, prefix="10.200.1.0/24")

    ipam.network(name=vlans.vlan_inband_mgmt, prefix="10.254.1.0/24")

    design.ipams[0] = ipam
    return ipam
