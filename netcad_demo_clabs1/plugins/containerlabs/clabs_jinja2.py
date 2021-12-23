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
