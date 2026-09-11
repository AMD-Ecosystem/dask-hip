#!/usr/bin/env bash
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

# Build the dask-hip wheel "matrix" inside a manylinux container.
#
# The matrix has one entry, and that is the point: dask-hip is pure Python, so
# setuptools tags the wheel py3-none-any and one build serves every supported
# interpreter. Its compiled siblings (hipMM, hipRAFT, hipVS) need a pass per
# interpreter; this one does not, and the driver exists so the builder wrapper
# calls the same script name they do and so the py3-none-any tag is asserted
# rather than assumed.
#
# The interpreter still matters for one thing: it decides which /opt/python is
# on PATH while the wheel is built, and a build that silently fell back to the
# manylinux system python would be harder to reproduce.
#
# Required environment variables:
#   PROJECT_ID, SRC_DIR, BUILD_DIR, BUILD_ARTIFACTS_DIR
#   Everything else build-wheels.sh reads is passed through untouched.
#
# Optional environment variables:
#   DASK_HIP_BUILD_ABI -- the /opt/python entry to build with
#                         (default: cp312-cp312)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${PROJECT_ID:?PROJECT_ID must be set}"
: "${SRC_DIR:?SRC_DIR must be set}"
: "${BUILD_DIR:?BUILD_DIR must be set}"
: "${BUILD_ARTIFACTS_DIR:?BUILD_ARTIFACTS_DIR must be set}"

# build-wheels.sh reads these from the environment, and a caller that assigned
# them without exporting would otherwise hand it nothing.
export PROJECT_ID SRC_DIR BUILD_DIR BUILD_ARTIFACTS_DIR

mkdir -p "${BUILD_ARTIFACTS_DIR}"

build_abi=${DASK_HIP_BUILD_ABI:-cp312-cp312}
python_bin="/opt/python/${build_abi}/bin"

if [ ! -x "${python_bin}/python" ]; then
  echo "ERROR: ${python_bin}/python is missing." >&2
  exit 1
fi

echo "=============================================================="
echo "amd_dask_hip, built once with ${build_abi}"
echo "=============================================================="

PATH="${python_bin}:${PATH}" "${SCRIPT_DIR}/build-wheels.sh"

### verify the build produced the tag it promised
#
# A py3-none-any wheel is what makes the single pass legitimate. Were the
# package ever to grow a compiled extension, setuptools would quietly tag the
# wheel for the building interpreter instead, and every other interpreter in
# the test matrix would then fail to install it, a stage and a container later.

shopt -s nullglob

echo "=============================================================="
echo "Wheels in ${BUILD_ARTIFACTS_DIR}"
echo "=============================================================="

found=("${BUILD_ARTIFACTS_DIR}"/amd_dask_hip-*-py3-none-any.whl)
printf '  %-14s %d wheel(s)\n' "py3-none-any" "${#found[@]}"

if [ ${#found[@]} -eq 0 ]; then
  echo "ERROR: no py3-none-any amd_dask_hip wheel was produced." >&2
  echo "Wheels that are present:" >&2
  ls -1 "${BUILD_ARTIFACTS_DIR}" >&2 || true
  exit 1
fi

unexpected=("${BUILD_ARTIFACTS_DIR}"/amd_dask_hip-*-cp*.whl)
if [ ${#unexpected[@]} -gt 0 ]; then
  echo "ERROR: amd_dask_hip was tagged for a specific interpreter:" >&2
  printf '  - %s\n' "${unexpected[@]}" >&2
  echo "One pass only serves every interpreter while the wheel stays pure Python." >&2
  exit 1
fi

echo "Wheel build complete."
