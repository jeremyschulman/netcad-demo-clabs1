# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["netcad_demo_clabs1"]

package_data = {"": ["*"]}

setup_kwargs = {
    "name": "netcad-demo-clabs1",
    "version": "0.1.0",
    "description": "NetCadCam demonstration using ContainerLabs",
    "long_description": None,
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
