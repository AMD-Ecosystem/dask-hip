#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

"""Pre-generate CLI documentation RST using sphinx-click internals.

Must be run on a system with dask-hip and all AMD dependencies installed.

Prerequisites:
    pip install sphinx-click

Usage:
    cd docs_amd/reference/dask_cuda_api
    python generate_cli_docs.py
"""

import os

import click
from sphinx_click.ext import _format_command

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUBS_DIR = os.path.join(SCRIPT_DIR, "stubs")

COMMANDS = [
    {
        "import": "dask_cuda.cli",
        "attr": "worker",
        "prog": "dask cuda worker",
        "output": os.path.join(STUBS_DIR, "cli_worker.rst"),
    },
    {
        "import": "dask_cuda.cli",
        "attr": "config",
        "prog": "dask cuda config",
        "output": os.path.join(STUBS_DIR, "cli_config.rst"),
    },
]


def generate_rst(module_name, attr_name, prog_name):
    """Generate RST content for a Click command using sphinx-click."""
    mod = __import__(module_name, fromlist=[attr_name])
    cmd = getattr(mod, attr_name)
    ctx = click.Context(cmd, info_name=prog_name)
    lines = list(_format_command(ctx, nested="none"))
    return "\n".join(lines) + "\n"


def main():
    for spec in COMMANDS:
        print(f"Generating CLI docs for {spec['prog']}...")
        rst = generate_rst(spec["import"], spec["attr"], spec["prog"])
        with open(spec["output"], "w") as f:
            f.write(rst)
        print(f"  -> {spec['output']}")

    print("\nCLI docs generated. Review and commit:")
    print("  git add stubs/cli_*.rst")
    print("  git commit -m 'Regenerate CLI documentation'")


if __name__ == "__main__":
    main()
