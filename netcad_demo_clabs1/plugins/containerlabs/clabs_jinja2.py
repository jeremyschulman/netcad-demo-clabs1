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

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["create_j2env"]


# -----------------------------------------------------------------------------
#
#                               CODE BEGINS
#
# -----------------------------------------------------------------------------


def create_j2env(template_dir) -> jinja2.Environment:
    """
    Create a Jinja2 enviornment instance used when template building the containerlab
    topology file.

    Parameters
    ----------
    template_dir: str
        The file path where the Jinja2 template file is located.

    Returns
    -------
    A Jinja2 enviornment instance that will be used to template build the
    containerlabs topology file.
    """
    env = jinja2.Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        loader=jinja2.FileSystemLoader([template_dir]),
        undefined=jinja2.StrictUndefined,
    )

    return env
