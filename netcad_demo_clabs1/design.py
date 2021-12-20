from netcad.design_services import Design
from netcad.topology import TopologyService
from netcad.vlan.vlan_design_service import VlansDesignService

from .roles import CoreSwitch, Acc01Switch, Acc02Switch


def create_design(design: Design) -> Design:

    core = CoreSwitch(name="core01")
    sw1 = Acc01Switch(name="acc01")
    sw2 = Acc02Switch(name="acc02")
    all_devs = [core, sw1, sw2]

    design.add_devices(*all_devs)
    topo_svc = design.services["topology"] = TopologyService(network=design.name)
    topo_svc.add_devices(*all_devs)

    vlans_svc = design.services["vlans"] = VlansDesignService()
    vlans_svc.add_devices(*all_devs)

    design.update()

    return design
