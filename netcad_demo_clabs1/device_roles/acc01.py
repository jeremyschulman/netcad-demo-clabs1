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
# Private Imports
# -----------------------------------------------------------------------------

from ..cabling import DemoCabling
from ..profiles.trunks import AccToCoreUplink
from ..profiles import access
from .access import AccessSwitch


# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["Acc01Switch"]

# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


class Acc01Switch(AccessSwitch):
    sort_key = (1, 1)


if_defs = Acc01Switch.interfaces

# -----------------------------------------------------------------------------
#                        Host facing ports
# -----------------------------------------------------------------------------

if_defs["Ethernet1"].profile = access.Printer(desc="HR-printer")
if_defs["Ethernet2"].profile = access.Phone(desc="Bob H. phone")
if_defs["Ethernet3"].profile = access.Phone(desc="Alice C. phone")

# -----------------------------------------------------------------------------
#                        Uplink ports to core switch
# -----------------------------------------------------------------------------

with if_defs["Ethernet7"] as eth7, if_defs["Ethernet8"] as eth8:
    eth7.profile = AccToCoreUplink()
    eth7.cable_id = DemoCabling.uplink_core01_acc01_1

    eth8.profile = AccToCoreUplink()
    eth8.cable_id = DemoCabling.uplink_core01_acc01_2
