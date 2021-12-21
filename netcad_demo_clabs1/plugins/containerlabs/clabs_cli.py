# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import Tuple
from pathlib import Path

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

import click

from netcad.cli.netcad.cli_netcad_main import cli
from netcad.cli.common_opts import opt_designs
from netcad.design_services import load_design

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .consts import DEFAULT_TOPOLOGY_TEMPLATE
from .clabs_jinja2 import create_j2env


@cli.group(name="clabs")
def clig_clabs():
    """ContainerLabs subcommands ..."""


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
    Create containerlabs topology file
    """

    template_dir = str(template_file.parent)
    env = create_j2env(template_dir)

    template = env.get_template(template_file.name)

    for design_name in designs:
        design_obj = load_design(design_name)
        file_content = template.render(design=design_obj)
        print(file_content)
