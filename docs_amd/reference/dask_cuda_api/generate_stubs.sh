#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Generate Python API stubs for dask-hip documentation.
# Must be run on a system with dask-hip and all AMD dependencies installed.
#
# Prerequisites:
#   pip install mypy  # provides stubgen
#
# Usage:
#   cd docs_amd/reference/dask_cuda_api
#   bash generate_stubs.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STUBS_DIR="${SCRIPT_DIR}/stubs"

echo "Cleaning existing stubs..."
rm -rf "${STUBS_DIR}/dask_cuda"

echo "Generating stubs with stubgen..."
stubgen \
    --include-docstrings \
    -p dask_cuda \
    -o "${STUBS_DIR}"

echo "Removing stubs for benchmarks and tests..."
rm -rf "${STUBS_DIR}/dask_cuda/benchmarks"
rm -rf "${STUBS_DIR}/dask_cuda/tests"

echo "Stubs generated in ${STUBS_DIR}/dask_cuda/"

echo ""
echo "Generating CLI documentation RST..."
python "${SCRIPT_DIR}/generate_cli_docs.py"

echo ""
echo "Review the generated stubs and CLI docs, then commit:"
echo "  git add stubs/"
echo "  git commit -m 'Regenerate Python API stubs and CLI docs'"
