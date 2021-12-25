# -*- coding: utf-8 -*-
from setuptools import setup

packages = [
    "netcad_demo_clabs1",
    "netcad_demo_clabs1.designs",
    "netcad_demo_clabs1.device_roles",
    "netcad_demo_clabs1.plugins",
    "netcad_demo_clabs1.plugins.containerlabs",
    "netcad_demo_clabs1.profiles",
]

package_data = {"": ["*"]}

setup_kwargs = {
    "name": "netcad-demo-clabs1",
    "version": "0.1.0",
    "description": "NetCadCam demonstration using ContainerLabs",
    "long_description": '# Demo - NetCadCam using ContainerLab\n\nThis respository contains a "Hello, world!" example of using  the NetCadCam\ntoolkit.  The  network testbed is a [containerlab](https://containerlab.srlinux.dev/) system comprised of three\nArista cEOS instances.\n\nThe primary purpose of this repo is to allow folks interested in the NetCadCam\nproject to see a working example of design files and how they are used to\nvalidate the operational state of the network.  Inclusively:\n\n  * The ability to generate the network checks and validate the operational state of the network\n  * The ability to generate the cEOS configuration files\n  * The ability to generate the containerlabs topology file\n  * See how NetCadCam can be extended to include containerlab CLI features\n\n',
    "author": "Jeremy Schulman",
    "author_email": None,
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "python_requires": ">=3.8,<4.0",
}


setup(**setup_kwargs)
