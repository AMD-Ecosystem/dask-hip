.. SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
.. SPDX-License-Identifier: MIT

.. meta::
   :description: dask-hip system requirements
   :keywords: Dask, GPU, HIP, ROCm, ROCm-DS, AMD, requirements, compatibility

.. _system-requirements:

*******************
System requirements
*******************

This page lists the system requirements for using ``dask-hip``.

* Operating Systems: many_linux version 2.28. Ubuntu 22.04 is recommended. 
* ROCm version: 7.2.0
* Supported AMD GPUs:

  - MI350X / MI355X (GPU target gfx950)
  - MI300A / MI300X (GPU target gfx942)
  - MI250X / MI250 / MI210 (GPU target gfx90a)

* Python versions: 3.10, 3.11, 3.12

Conda or virtual environment
-----------------------------

A Conda installation or Python virtual environment is recommended for managing dependencies, such as `Miniforge <https://conda-forge.org/download/>`_ as a minimal Conda distribution.
