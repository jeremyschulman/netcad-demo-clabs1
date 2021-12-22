from pathlib import Path
from netcad.device.l3_interfaces import InterfaceL3


class ClabAutoManagement(InterfaceL3):
    desc = "dynamically assigned by containerlab"
    is_reserved = True
    template = Path("interface_ma0.jinja2")
