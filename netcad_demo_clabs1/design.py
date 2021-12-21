from netcad.design_services import Design
from netcad.topology import TopologyDesignService
from netcad.vlan.vlan_design_service import VlansDesignService

from .device_roles import CoreSwitch, Acc01Switch, Acc02Switch


def create_design(design: Design) -> Design:

    core = CoreSwitch(name="core01")
    sw1 = Acc01Switch(name="acc01")
    sw2 = Acc02Switch(name="acc02")

    all_devs = [core, sw1, sw2]

    design.add_devices(*all_devs).add_services(
        TopologyDesignService(topology_name=design.name, devices=all_devs),
        VlansDesignService(devices=all_devs),
    ).update()

    return design
