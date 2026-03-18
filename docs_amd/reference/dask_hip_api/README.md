<!-- SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc. -->
<!-- SPDX-License-Identifier: MIT -->

# Python API Stubs for Documentation

The `stubs/` directory contains `.pyi` stub files used by `sphinx-autoapi` to generate
Python API documentation without requiring dask-hip and its AMD-specific dependencies
to be importable at doc build time.

## When to regenerate

Regenerate stubs whenever the public API changes (new classes, functions, parameter
changes, docstring updates).

## How to regenerate

The stubs must be generated on a system with AMD GPUs and a working dask-hip installation
(including `amdsmi`, `hip-python`, `numba-hip`, etc.).

1. Install dask-hip and all dependencies:

   ```bash
   pip install -e ".[test]" --extra-index-url=https://pypi.amd.com/simple
   pip install mypy sphinx-click  # provides stubgen and CLI doc generation
   ```

2. Run the generation script:

   ```bash
   cd docs_amd/reference/dask_hip_api
   bash generate_stubs.sh
   ```

   This generates both Python API stubs (`.pyi` files) and CLI documentation
   RST files (`cli_worker.rst`, `cli_config.rst`) in the `stubs/` directory.

3. Review the generated stubs and commit them:

   ```bash
   git add stubs/
   git commit -m "Regenerate Python API stubs and CLI docs"
   ```

## Manual overrides

If `stubgen` produces incorrect or incomplete stubs for certain modules, you can
manually edit the `.pyi` files in `stubs/`. These edits will be preserved until
the next regeneration, so document any manual changes here.
