# SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../"))

try:
    from dask_cuda import __version__

    version_number = __version__
except ImportError:
    version_number = "0.0.0.dev"

left_nav_title = f"dask-hip {version_number} documentation"

project = "dask-hip"
author = "Advanced Micro Devices, Inc."
copyright = "Copyright (c) 2026 Advanced Micro Devices, Inc. All rights reserved."
version = version_number
release = version_number
setting_all_article_info = True
all_article_info_os = ["linux"]
all_article_info_author = ""

external_projects_current_project = "dask-hip"

html_context = {"docs_header_version": "26.03"}
html_theme = "rocm_docs_theme"
html_theme_options = {
    "flavor": "rocm-ds",
    "repository_url": "https://github.com/AMD-AIOSS/dask-hip/",
}

external_toc_path = "./sphinx/_toc.yml"

extensions = [
    "rocm_docs",
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

# -- sphinx-autoapi configuration -------------------------------------------
autoapi_type = "python"
autoapi_dirs = [
    os.path.join(os.path.dirname(__file__), "reference", "dask_cuda_api", "stubs"),
]
autoapi_ignore = ["*/__pycache__/*"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"
autoapi_keep_files = False
autoapi_add_toctree_entry = False
autoapi_generate_api_docs = False

exclude_patterns = [
    "reference/dask_cuda_api/README.md",
]

myst_heading_anchors = 4
autosectionlabel_prefix_document = True
napoleon_preprocess_types = True
autodoc_typehints = "description"

suppress_warnings = [
    "etoc.toctree",
    "intersphinx.external",
]

source_suffix = {
    ".rst": "restructuredtext",
}
