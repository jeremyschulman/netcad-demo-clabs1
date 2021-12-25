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

from netcad.device import Device

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["AnyDevice", "AnyContainerEosDevice"]


# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------


class AnyDevice(Device):
    """
    Baseclass for any device used in the containerlab design.

    Each device in this design will have a set of attributes that are used
    to calculate various design aspects.

    Attributes
    ----------
    device_base_name: str
        Used when auto-generating the device hostname value.  For example, the
        "core" device-role subclass will set this value to "core" so that all
        hostnames begin with "core".

    net_id: int
        A positive integer value, starting with 1, that is used to uniquely
        identify the network in the design.  The network Id value is globally
        unique across all designs.

    bld_id: int
        A posivitve integer value, starting with 1, that represents the building
        Id value.  Building Id values are globally unique; meaning there is only
        one building Id = 1.

    flr_id: int
        A positive integer value, starting with 1, that represents the building
        floor Id.  A floor id is locally significant within the building;
        meaning that multiple building will have a flr_id 1, for example.

    dev_id: int
        A positive integer value, starting with 1, that represents the
        device-role Id value within the device-class.  For example, if a design
        has muliple access-switch devices, the first one would have a dev_id=1,
        the second would have a dev_id=2.  In the same design, the first core
        device, a different device-role, would have a dev_id=1.

    sort_key: tuple
        This baseclass uses a sort-key methodology based on a "file-rank"
        chessboard, where the tuple (0, 0) would represent the top-left most
        corner. Each device-role, for example a "core switch" will define their
        own sort-key such that when displaying devices in reports, diagrams, and
        such the devices will be sort-ordered according to this sort-key method.
    """

    sort_key = tuple()  # (file, rank)
    device_base_name: str = ""

    def __init__(self, dev_id: int, bld_id: int, flr_id: int, **kwargs):
        """
        Create a new Device instance, using the various design-specific ID
        values to formulate the unqiue device hostname and sort-key calues.

        Parameters
        ----------
        dev_id: int
            The device-Id as described.

        bld_id: int
            The building Id as described.

        flr_id: int
            The floor Id as described.

        Other Parameters
        ----------------
        These are any other parameters that the Device superclass would accept.
        At this time, none are expected; but leaving this parameter here for
        potential future use.
        """

        # dynamically build the hostname based on the "id" parameters
        name = f"{self.device_base_name}{dev_id:02}.{bld_id}{flr_id}"
        super().__init__(name=name, **kwargs)

        # set the "(file,rank)" sort key based on the base-class file and the
        # dev-id rank
        self.sort_key = (self.sort_key[0], dev_id)

        self.bld_id = bld_id
        self.flr_id = flr_id
        self.dev_id = dev_id

    def __lt__(self, other: "AnyDevice"):
        """used for sorrting devices amoung each other"""
        return self.sort_key < other.sort_key


class AnyContainerEosDevice(AnyDevice):
    """
    Baseclass for any Arista cEOS based device used in the containerlab design.
    """

    product_model = "cEOSLab"
    device_type = "cEOS-8"
    os_name = "eos"
