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
    sort_key = tuple()  # (file, rank)
    device_base_name: str = ""

    def __init__(self, dev_id: int, bld_id: int, fl_id: int, **kwargs):

        # dynamically build the hostname based on the "id" parameters
        name = f"{self.device_base_name}{dev_id:02}.{bld_id}{fl_id}"
        super().__init__(name=name, **kwargs)

        # set the "(file,rank)" sort key based on the base-class file and the
        # dev-id rank
        self.sort_key = (self.sort_key[0], dev_id)

        self.bld_id = bld_id
        self.flr_id = fl_id
        self.dev_id = dev_id

    def __lt__(self, other: "AnyDevice"):
        return self.sort_key < other.sort_key


class AnyContainerEosDevice(AnyDevice):
    product_model = "cEOSLab"
    device_type = "cEOS-8"
    os_name = "eos"
