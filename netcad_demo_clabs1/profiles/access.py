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

from pathlib import Path

from netcad.device.l2_interfaces import InterfaceL2Access

from netcad_demo_clabs1.vlans import vlan_printers, vlan_phones, vlan_employee_desk
from netcad_demo_clabs1.profiles.phy_port import port_ebra


class Printer(InterfaceL2Access):
    port_profile = port_ebra
    vlan = vlan_printers
    template = Path("interface_access.jinja2")


class Phone(InterfaceL2Access):
    port_profile = port_ebra
    vlan = vlan_phones
    template = Path("interface_access.jinja2")


class DeskUser(InterfaceL2Access):
    port_profile = port_ebra
    vlan = vlan_employee_desk
    template = Path("interface_access.jinja2")
