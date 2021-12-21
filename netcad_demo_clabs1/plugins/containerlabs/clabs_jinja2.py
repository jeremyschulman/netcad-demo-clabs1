# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import jinja2
from netcad.device import DeviceInterface

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["create_j2env"]

# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


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


def create_j2env(template_dir):

    env = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        loader=jinja2.FileSystemLoader([template_dir]),
        undefined=jinja2.StrictUndefined,
    )

    env.filters["clab_intfname"] = j2filter_clab_ifname
    env.tests["is_clab_dataport"] = j2test_is_dataport

    return env
