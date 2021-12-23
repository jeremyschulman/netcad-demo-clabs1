from netcad.design_services import Design
from netcad.ipam import IPAM

from . import vlans


def create_site_ipam(design: Design, bld_id: int, flr_id: int) -> IPAM:

    ipam = IPAM(name=design.name)

    ipam.network("OOB", prefix="172.20.20.0/24")

    ipam.network(name=vlans.vlan_phones, prefix="10.10.1.0/24")
    ipam.network(name=vlans.vlan_printers, prefix="10.10.2.0/24")
    ipam.network(name=vlans.vlan_media_iptvs, prefix="10.10.3.0/24")

    ipam.network(name=vlans.vlan_inband_mgmt, prefix="10.254.1.0/24")

    design.ipams[0] = ipam
    return ipam
