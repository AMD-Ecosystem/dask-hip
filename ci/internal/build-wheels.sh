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

# Build the dask-hip wheel (amd-dask-hip).
#
# One wheel, no matrix: dask-hip is pure Python, so setuptools tags it
# py3-none-any and every supported interpreter installs the same file.
# build-wheels-manylinux.sh is the driver that says so and checks it.
#
# Required environment variables:
#   PROJECT_ID, SRC_DIR, BUILD_DIR, BUILD_ARTIFACTS_DIR
#
# Optional environment variables:
#   CI_INTERNAL_CREATE_TESTS_TARBALL -- '1' packs the tests tarball the tester
#               images consume (default: 0). The wheel excludes
#               dask_cuda/tests and dask_cuda/benchmarks, so the suite has to
#               travel separately.

set -euxo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/_wheel-helpers.sh"
: "${PROJECT_ID:?PROJECT_ID must be set}"
: "${SRC_DIR:?SRC_DIR must be set}"
: "${BUILD_DIR:?BUILD_DIR must be set}"
: "${BUILD_ARTIFACTS_DIR:?BUILD_ARTIFACTS_DIR must be set}"

src_dir=${SRC_DIR}/${PROJECT_ID}
build_dir=${BUILD_DIR}/${PROJECT_ID}
tests_tarball_name="${PROJECT_ID}-tests.tar.gz"

case "${CI_INTERNAL_CREATE_TESTS_TARBALL:-0}" in
  1 | true | yes | on) create_tests_tarball="1" ;;
  *) create_tests_tarball="" ;;
esac

mkdir -p "${BUILD_ARTIFACTS_DIR}"

# The tree stays after the build, unlike the compiled projects': it is what the
# tests tarball carries and what the tester runs pytest out of.
rm -rf "${build_dir}"
mkdir -p "$(dirname "${build_dir}")"
cp -a "${src_dir}" "${build_dir}"

# WHEEL_BUILD_ROOT is the parent, and the package is the checkout itself, so
# the helper's log file is named after the project rather than after '.'.
export WHEEL_BUILD_ROOT="${BUILD_DIR}"

wheels_build_env=$(mktemp -d)
python3 -m venv ${wheels_build_env}
. ${wheels_build_env}/bin/activate

    . "${SCRIPT_DIR}/_install-build-deps.sh"

    build_setuptools_wheel "${PROJECT_ID}"

deactivate
rm -rf ${wheels_build_env}

#### test archive

# The tester image extracts this at / and runs ci/internal/test-wheels*.sh out
# of the tree it carries, so the archive keeps absolute paths. No dev venv
# travels with it: there is nothing compiled here, and test-wheels.sh builds
# its own venv per interpreter anyway.
if [ -n "${create_tests_tarball:-}" ]; then
  tar --exclude=.git -czf "${BUILD_ARTIFACTS_DIR}/${tests_tarball_name}" \
    "${build_dir}"
  du -sh "${BUILD_ARTIFACTS_DIR}/${tests_tarball_name}"
fi
