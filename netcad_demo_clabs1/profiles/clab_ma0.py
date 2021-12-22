from pathlib import Path
from netcad.device.l3_interfaces import InterfaceL3


class Management0(InterfaceL3):
    desc = "connected to clab"
    template = Path("interface_ma0.jinja2")
