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

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click
import jinja2

from netcad.design_services import Design
from netcad.cli.netcad.cli_netcad_main import cli
from netcad.cli.common_opts import opt_designs
from netcad.design_services import load_design
from netcad.topology import TopologyServiceLike, NoValidateCabling

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
@click.option(
    "--save-dir",
    "save_dir",
    type=click.Path(
        path_type=Path, resolve_path=True, exists=True, dir_okay=True, file_okay=False
    ),
)
@click.option(
    "--dummy-bridge",
    help="name of dummy bridge to force creation of device interfaces",
    default="br-dummy",
)
def clig_clabs_topology(
    designs: Tuple[str], template_file: Path, save_dir: Path, dummy_bridge: str
):
    """
    Create containerlab topology file.
    """

    template_dir = str(template_file.parent)
    env = create_j2env(template_dir)
    template = env.get_template(template_file.name)

    for design_name in designs:
        design_obj = load_design(design_name)
        topo_content = render_topology_content(template, design_obj, dummy_bridge)

        if save_dir:
            topo_file = save_dir / (design_obj.name + ".clab.yaml")
            with topo_file.open("w+") as ofile:
                print(f"SAVE: {ofile.name}")
                ofile.write(topo_content)

        else:
            print(topo_content)


def render_topology_content(
    template: jinja2.Template, design_obj: Design, dummy_br_name: str
) -> str:
    """
    Generate the topology content for a given design.

    Parameters
    ----------
    template: Template
        The jinja2 template instance that will be used for rendeing purposes.

    design_obj: Design
        The design instance that is used to formulate the variables that
        are passed to the Template for rendering.

    dummy_br_name: str
        The User define "dummy bridge" name that is used to define interfaces in
        the containerlab topology so that they exist as virtual-ethernet
        interfaces in Linux.

    Returns
    -------
    str
        The topology content that needs to be saved to a file.
    """
    # TODO: should not use hardcoded 'topology', but for demo ok.
    topo_svc: TopologyServiceLike = design_obj.services["topology"]

    # create the 'cabling' list of actual ports that are to be cabled
    # together in the topology.

    cabled_ports = set()
    fake_br_id = 0
    cabling = []
    used_uncabled = []
    unused_ports = []

    for cable_id, endpoints in topo_svc.cabling.cables.items():
        end_a, end_b = sorted(endpoints, key=lambda e: (e.device, e))
        cabled_ports.update((end_a, end_b))

        if end_b.cable_port_id is NoValidateCabling:
            side_b = f"{dummy_br_name}:{fake_br_id}"
            fake_br_id += 1
        else:
            side_b = f"{end_b.device.name}:{end_b.short_name.lower()}"

        cabling.append((f"{end_a.device.name}:{end_a.short_name.lower()}", side_b))

    for dev_obj in design_obj.devices.values():
        if dev_obj.is_pseudo:
            continue

        for ifobj in dev_obj.interfaces.values():
            if ifobj in cabled_ports:
                continue

            if ifobj.used and (ifobj.profile.is_mgmt_only or ifobj.profile.is_virtual):
                continue

            add_to = used_uncabled if ifobj.used else unused_ports

            add_item = (
                f"{ifobj.device.name}:{ifobj.short_name.lower()}",
                fake_br_id,
            )

            add_to.append(add_item)
            fake_br_id += 1

    devices = [dev for dev in design_obj.devices.values() if not dev.is_pseudo]

    return template.render(
        design=design_obj,
        devices=devices,
        cabled_ports=cabling,
        uncabled_ports=used_uncabled,
        unused_ports=unused_ports,
    )
