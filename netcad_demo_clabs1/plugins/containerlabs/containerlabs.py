# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import Tuple
from pathlib import Path

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click
import jinja2

from netcad.device import DeviceInterface
from netcad.cli.netcad.cli_netcad_main import cli
from netcad.cli.common_opts import opt_designs
from netcad.design_services import load_design


# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------

_DEFAULT_TOPOLOGY_TEMPLATE = Path(__file__).parent / "topology_template.jinja2"


@cli.group(name="clabs")
def clig_clabs():
    """ContainerLabs subcommands ..."""


@jinja2.pass_context
def j2filter_clab_ifname(ctx, intf_obj: DeviceInterface) -> str:
    """
    This function converts the device interface name into a value that can be
    used by the ContainerLabs system.  For example, "cEOS" devices have actual
    interfaces with "Ethernet", and the ContainerLabs topology file needs these
    to be in the form "eth" or "et" depending on the setup of the topology file.

    Parameters
    ----------
    ctx
    intf_obj: DeviceInterface
        The device interface object

    Returns
    -------
    The interface string value consumable by ContainerLabs topology file.
    """

    # TODO: support more than cEOS
    os_name = intf_obj.device.os_name
    if os_name != "eos":
        raise RuntimeError("ContainerLabs plugin only supports cEOS at this time")

    intf_port = intf_obj.port_numbers[0]
    return f"eth{intf_port}"


def j2test_is_dataport(intf_obj: DeviceInterface) -> bool:
    # TODO: support more than just cEOS
    if_name = intf_obj.name
    return if_name.startswith("Eth")


@clig_clabs.command("topology")
@opt_designs()
@click.option(
    "--template",
    "template_file",
    help="path to specific template file",
    default=_DEFAULT_TOPOLOGY_TEMPLATE,
    type=click.Path(path_type=Path, resolve_path=True, exists=True),
)
def clig_clabs_topology(designs: Tuple[str], template_file: Path):
    """
    Create containerlabs topology file
    """

    template_dir = str(template_file.parent)

    env = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        loader=jinja2.FileSystemLoader([template_dir]),
        undefined=jinja2.StrictUndefined,
    )

    env.filters["clab_intfname"] = j2filter_clab_ifname
    env.tests["is_clab_dataport"] = j2test_is_dataport

    template = env.get_template(template_file.name)

    for design_name in designs:
        design_obj = load_design(design_name)
        file_content = template.render(design=design_obj)
        print(file_content)


def plugin_init(config: dict):
    pass
