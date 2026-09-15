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

# Install test dependencies for dask-hip.
# Meant to be sourced, not executed directly.
#
# Required environment variables:
#   BUILD_ARTIFACTS_DIR -- directory containing pre-built dependency wheels
#
# Optional environment variables:
#   CUPY_VERSION -- pins amd-cupy; CI sets it from the builder-tester
#                   _envs/rocmds/<branch> env file, and a bare checkout without
#                   it installs unpinned
#   HIPMM_VERSION, HIPDF_VERSION -- the same, for the rmm and cudf wheels

set -euo pipefail

pip install --upgrade pip

# The [project.optional-dependencies] test extra, spelled out: the wheel is
# installed by name from the pool, and pip does not resolve an extra of a
# distribution it takes from --find-links without being asked for it.
pip install pytest pytest-cov pytest-csv pytest-timeout \
    "pytest-rerunfailures!=16.0.0" psutil pyarrow

# amd-cupy is what the spilling and device-array suites allocate through, and
# amd-libhipmm/amd-hipmm provide the rmm those and the RMM-backed allocator
# suites import. The rocm-bindings-* / hip-python-interop set stays unpinned:
# their version leads with the ROCm version of the base image, which no env key
# names.
#
# --no-deps throughout, here and below: this package's own distribution pins the
# legacy hip-python ones, and pip would pull it in as a dependency of
# amd-distributed-hipucxx below and displace the rocm-bindings wheels with them.
pip install --no-deps \
    --find-links "${BUILD_ARTIFACTS_DIR}" \
    "amd-cupy${CUPY_VERSION:+==${CUPY_VERSION}}" \
    "amd-libhipmm${HIPMM_VERSION:+==${HIPMM_VERSION}}" \
    "amd-hipmm${HIPMM_VERSION:+==${HIPMM_VERSION}}" \
    rocm-bindings-core \
    rocm-bindings-hip \
    rocm-bindings-compiler \
    hip-python-interop

# The cudf and ucxx stack, which the suites guarding on cudf, dask_cudf, ucxx
# and distributed_ucxx need to run instead of skipping.
#
# Optional, unlike the set above: these are upstream components rather than
# this one's own dependencies, and every suite that uses them already guards
# itself with pytest.importorskip, so an upstream build that did not publish
# costs those suites rather than the run.
#
# The ucxx distributions are deliberately unpinned. UCXX_VERSION is 0.2.0 in
# the env file, the hip-ucxx checkout carries 00.01.00 and amd-raft-dask asks
# for ==0.1.*, so any pin here would be unsatisfiable against one of them.
if ! pip install --no-deps \
        --find-links "${BUILD_ARTIFACTS_DIR}" \
        "amd-libhipdf${HIPDF_VERSION:+==${HIPDF_VERSION}}" \
        "amd-pylibhipdf${HIPDF_VERSION:+==${HIPDF_VERSION}}" \
        "amd-hipdf${HIPDF_VERSION:+==${HIPDF_VERSION}}" \
        "amd-dask_hipdf${HIPDF_VERSION:+==${HIPDF_VERSION}}" \
        amd-libhipucxx amd-hipucxx amd-distributed-hipucxx; then
    echo "WARNING: cudf/ucxx stack unavailable; the suites importing it will skip."
fi
