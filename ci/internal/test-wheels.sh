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

# Test the dask-hip wheel in an isolated venv, using the interpreter on PATH.
#
# The suite lives in dask_cuda/tests, which the wheel excludes, so it is run
# out of the checkout the tests tarball carries while the package under test is
# the installed wheel.
#
# Required environment variables:
#   PROJECT_ID, BUILD_DIR, BUILD_ARTIFACTS_DIR, ARTIFACTS_DIR
#
# Optional environment variables:
#   DASK_HIP_TEST_RESULTS_SUFFIX -- appended to the pytest output dir and the
#               results CSV name. test-wheels-manylinux.sh sets it per
#               interpreter, since the passes share this checkout and this
#               artifacts dir.
#   DASK_HIP_VERSION -- pins the wheel installed from BUILD_ARTIFACTS_DIR

set -euxo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${PROJECT_ID:?PROJECT_ID must be set}"
: "${BUILD_DIR:?BUILD_DIR must be set}"
: "${BUILD_ARTIFACTS_DIR:?BUILD_ARTIFACTS_DIR must be set}"
: "${ARTIFACTS_DIR:?ARTIFACTS_DIR must be set}"

source "${SCRIPT_DIR}/_test-helpers.sh"
source "${SCRIPT_DIR}/_wheel-helpers.sh"

wheels_test_env=$(mktemp -d)
python3 -m venv "${wheels_test_env}"
. "${wheels_test_env}/bin/activate"

  pip install --upgrade pip
  . "${SCRIPT_DIR}/_install-test-deps.sh"

  # No --no-index here, unlike the build: this install resolves the wheel's
  # own runtime dependencies for real.
  install_built_wheel -- \
    "amd_dask_hip[test,test_ucxx,test_hipdf]${DASK_HIP_VERSION:+==${DASK_HIP_VERSION}}"

  setup_dask_hip_test_env

  test_failures=0
  cd "${BUILD_DIR}/${PROJECT_ID}"

      results_suffix=${DASK_HIP_TEST_RESULTS_SUFFIX:+-${DASK_HIP_TEST_RESULTS_SUFFIX}}
      CSV_OUTPUT_DIR=${PROJECT_ID}_pytest_output${results_suffix}

      TIMEOUT_PER_TEST_SEC=300

      # --import-mode=append keeps the installed dask_cuda on the path ahead of
      # the checkout beside the tests, so the wheel is what gets exercised.
      run_tests dask_cuda/tests "${CSV_OUTPUT_DIR}" "${TIMEOUT_PER_TEST_SEC}" \
        "--timeout-method=thread --import-mode=append"

      result=$(merge_test_results "${CSV_OUTPUT_DIR}") || test_failures=1
      echo "$result" > "${ARTIFACTS_DIR}/${PROJECT_ID}-test-results-py${results_suffix}.csv"

deactivate
rm -rf "${wheels_test_env}"

exit "$test_failures"
