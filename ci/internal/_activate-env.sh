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

# Shared helpers: environment validation and build-environment activation.
# Meant to be sourced, not executed directly.
#
# Provides:
#   require_envs()                   - fails with a clear error if any named
#                                      variable is unset or empty
#   activate_dask_hip_venv()         - activates the dev venv
#   activate_dask_hip_conda_env()    - activates DASK_HIP_CONDA_ENV when set

set -euo pipefail

require_envs() {
    local missing=0
    for var in "$@"; do
        if [ -z "${!var:-}" ]; then
            echo "ERROR: required environment variable ${var} is not set." >&2
            missing=1
        fi
    done
    if [ "$missing" -ne 0 ]; then
        echo "ERROR: missing required environment variables (see above). Aborting." >&2
        exit 1
    fi
}


activate_dask_hip_venv() {
    . "${INSTALL_DIR}/venv/dask_hip_dev/bin/activate"
}


# Activates the conda env named by DASK_HIP_CONDA_ENV, if set.
#
# Returns 0 (and activates the env) when DASK_HIP_CONDA_ENV is set, 1 otherwise
# so callers can fall back to activate_dask_hip_venv.
#
# Required environment variables (when DASK_HIP_CONDA_ENV is set):
#   DASK_HIP_CONDA_ENV -- name of the conda environment to activate
#   CONDA_DIR          -- path to the conda installation
activate_dask_hip_conda_env() {
    if [ -n "${DASK_HIP_CONDA_ENV:-}" ]; then
        set +u # note: conda script may have unbound variables
        source "${CONDA_DIR}/etc/profile.d/conda.sh"
        conda activate "${DASK_HIP_CONDA_ENV}"
        set -u

        export LD_LIBRARY_PATH="${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH:-}"
        return 0
    fi
    return 1
}
