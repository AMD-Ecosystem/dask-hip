# shellcheck shell=bash
# MIT License
#
# Copyright (c) 2026 Advanced Micro Devices, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Install build dependencies for dask-hip.
# Meant to be sourced, not executed directly.
#
# The build runs with --no-build-isolation, so pip installs nothing from the
# package's own [build-system] requires: everything it declares has to be here.
# verify_build_requires() in _wheel-helpers.sh checks that.
#
# dask-hip is pure Python and builds through plain setuptools, so this is the
# whole list: no cmake, no Cython, and none of the ROCm-DS dependency wheels,
# which it needs at run time but not to produce a py3-none-any wheel.

set -euo pipefail

pip install --upgrade pip
pip install "setuptools>=64.0.0" wheel

# auditwheel only copies a pure-Python wheel through, but it is what stamps the
# platform tag consistently with the rest of the ROCm-DS pool.
pip install auditwheel patchelf
