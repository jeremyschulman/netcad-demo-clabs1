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

# =============================================================================
# This file contains the design for the "building 1, floor 2" network.
# =============================================================================

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from netcad.design_services import Design

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from .std_design import create_std_design

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["create_design"]


# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------


def create_design(design: Design) -> Design:
    """
    This function is the "design entry-point" for the building-1, floor-2
    network.  The name of this function **MUST** be `create_desgin` as this name
    is required so that the netcad tool can process it.

    Notes: Just the standard design here, so folks can experiment.

    Parameters
    ----------
    design: Design
        The design instance that needs to be filled in with the specifics of
        building-floor design

    Returns
    -------
    Design
        The updated design instance.
    """

    design = create_std_design(design)
    return design
