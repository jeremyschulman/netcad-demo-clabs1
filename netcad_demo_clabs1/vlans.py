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

from netcad.vlan import VlanProfile

vlan_native = VlanProfile(
    vlan_id=411, name="native_vlan", description="using different native vlan in demo"
)


vlan_phones = VlanProfile(vlan_id=10, name="Phones", description="Voip Phone ports")

vlan_printers = VlanProfile(vlan_id=20, name="Printers", description="Printer ports")

vlan_media_iptvs = VlanProfile(
    vlan_id=20, name="IPTV", description="IPTV set-top-boxes"
)

vlan_inband_mgmt = VlanProfile(
    vlan_id=911, name="Inband_MGMT", description="SVI used for inband management"
)

vlan_wifi_employee = VlanProfile(
    vlan_id=300, name="WIFI-Employee", description="For Employee Wifi"
)

vlan_wifi_visitor = VlanProfile(
    vlan_id=301, name="WIFI-Visitor", description="For Visitor Wifi"
)
