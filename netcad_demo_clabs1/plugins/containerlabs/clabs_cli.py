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
# System Imports
# -----------------------------------------------------------------------------

from typing import Tuple
from pathlib import Path
import re

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click

from netcad.cli.netcad.cli_netcad_main import cli
from netcad.cli.common_opts import opt_designs
from netcad.cli.device_inventory import get_devices_from_designs
from netcad.design_services import load_design
from netcad.topology import TopologyServiceLike

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .consts import DEFAULT_TOPOLOGY_TEMPLATE
from .clabs_jinja2 import create_j2env


@cli.group(name="clab")
def clig_clabs():
    """ContainerLabs subcommands ..."""


# -----------------------------------------------------------------------------
#
# netcad clabs topology
#
# -----------------------------------------------------------------------------


@clig_clabs.command("topology")
@opt_designs()
@click.option(
    "--template",
    "template_file",
    help="path to specific template file",
    default=DEFAULT_TOPOLOGY_TEMPLATE,
    type=click.Path(path_type=Path, resolve_path=True, exists=True),
)
def clig_clabs_topology(designs: Tuple[str], template_file: Path):
    """
    Create containerlab topology file.
    """

    template_dir = str(template_file.parent)
    env = create_j2env(template_dir)
    template = env.get_template(template_file.name)

    for design_name in designs:

        cabling = []
        used_uncabled = []
        unused_ports = []

        design_obj = load_design(design_name)

        # TODO: should not use hardcoded 'topology', but for demo ok.
        topo_svc: TopologyServiceLike = design_obj.services["topology"]

        # create the 'cabling' list of actual ports that are to be cabled
        # together in the topology.

        cabled_ports = set()

        for cable_id, endpoints in topo_svc.cabling.cables.items():
            end_a, end_b = sorted(endpoints, key=lambda e: (e.device, e))
            cabled_ports.update((end_a, end_b))

            cabling.append(
                (
                    f"{end_a.device.name}:{end_a.short_name.lower()}",
                    f"{end_b.device.name}:{end_b.short_name.lower()}",
                )
            )

        fake_br_id = 0

        for dev_obj in design_obj.devices.values():
            for ifobj in dev_obj.interfaces.values():
                if ifobj in cabled_ports:
                    continue

                add_to = used_uncabled if not ifobj.used else unused_ports
                add_item = (
                    f"{ifobj.device.name}:{ifobj.short_name.lower()}",
                    fake_br_id,
                )

                add_to.append(add_item)
                fake_br_id += 1

        file_content = template.render(
            design=design_obj,
            cabled_ports=cabling,
            uncabled_ports=used_uncabled,
            unused_ports=unused_ports,
        )
        print(file_content)


# -----------------------------------------------------------------------------
#
# netcad clabs etc-hosts
#
# -----------------------------------------------------------------------------


@clig_clabs.command("etc-hosts")
@opt_designs()
@click.option("--prefix", "clab_prefix", help="containerlab prefix", default="clab")
def clig_clabs_etchosts(designs: Tuple[str], clab_prefix):
    """
    Create an etc-hosts file with node.name only entries.

    The ContainerLabs system does not yet provide a means to create containers
    without prefix values.  For example, a node called "foo" in a topology will
    be created as container "clab-$topologoy.name-$node.name"

    This command generates a file that uses only the $node.name value so that a
    User can ssh/connect to the container device using the simple node name
    value.
    """

    device_objs = get_devices_from_designs(designs=designs)

    map_clab_known_hosts = {
        f"{clab_prefix}-{dev_obj.design.name}-{dev_obj.name}": dev_obj.name
        for dev_obj in device_objs
    }

    split_wspaces = re.compile(r"\s+")

    std_etc_hosts = list()

    with Path("/etc/hosts") as etc_in:
        for line in etc_in.read_text().splitlines():
            if not line or line.startswith("#"):
                continue

            ipaddr, hostname = split_wspaces.split(line, maxsplit=1)
            if not (simple_host := map_clab_known_hosts.get(hostname)):
                continue

            std_etc_hosts.append(f"{ipaddr}\t{simple_host}")

    print("\n".join(std_etc_hosts))


# -----------------------------------------------------------------------------
#
# netcad clabs copy-configs
#
# -----------------------------------------------------------------------------


@clig_clabs.command("cp-configs")
@opt_designs()
@click.option(
    "--path",
    "clab_dirpath",
    required=True,
    help="path to clab directory",
    type=click.Path(
        dir_okay=True, file_okay=False, exists=True, resolve_path=True, path_type=Path
    ),
)
def clig_clabs_copyconfigs(designs: Tuple[str], clab_dirpath: Path):
    """
    Generate the shell copy commands to copy the netcad generated config files
    into container flash area.  The default destination file name will be
    "netcad.cfg".  For now, this command is supports cEOS exclusively.

    The User is required to perform the copy command since sudo/root is
    required, for example:

        netcad clab cp-configs --path demo-clab1 | sudo bash -

    \f
    Parameters
    ----------
    designs:
        List of designs to process

    clab_dirpath: Path
        The root directory where the containerlab topology file is located.
    """
    device_objs = get_devices_from_designs(designs=designs)
    configs_dir = Path("configs")

    for dev_obj in device_objs:
        cfg_file = dev_obj.name + ".cfg"
        src_file = configs_dir / cfg_file
        dst_dir = (
            clab_dirpath / ("clab-" + dev_obj.design.name) / dev_obj.name / "flash"
        )
        dst_file = dst_dir / "netcad.cfg"
        print(f"cp {src_file.absolute()} {dst_file.absolute()}")
