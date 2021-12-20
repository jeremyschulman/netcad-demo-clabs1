from netcad.device import Device
from netcad.design_services import Design
from netcad.topology import TopologyService

from .roles import CoreSwitch, AccessSwitch
from netcad_demo_clabs1.cabling import DemoCabling


def create_design(design: Design) -> Design:

    core = CoreSwitch(name="core01")
    sw1 = AccessSwitch(name="acc01")
    sw2 = AccessSwitch(name="acc02")
    all_devs = [core, sw1, sw2]

    design.add_devices(*all_devs)
    _cable_access(sw1, sw2)

    topology = TopologyService(network=design.name)
    topology.add_devices(*all_devs)

    design.services["topology"] = topology
    design.update()

    return design


def _cable_access(sw1: Device, sw2: Device):

    with sw1.interfaces["Ethernet7"] as eth7, sw1.interfaces["Ethernet8"] as eth8:
        eth7.cable_id = DemoCabling.uplink_core01_acc01_1
        eth8.cable_id = DemoCabling.uplink_core01_acc01_2

    with sw2.interfaces["Ethernet7"] as eth7, sw2.interfaces["Ethernet8"] as eth8:
        eth7.cable_id = DemoCabling.uplink_core01_acc02_1
        eth8.cable_id = DemoCabling.uplink_core01_acc02_2
