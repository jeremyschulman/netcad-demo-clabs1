from pathlib import Path
from netcad.device.l3_interfaces import InterfaceL3


class Management0(InterfaceL3):
    template = Path("interface_ma0.jinja2")
