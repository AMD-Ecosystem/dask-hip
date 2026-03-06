.. SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
.. SPDX-License-Identifier: MIT

.. meta::
  :description: dask-hip documentation and API reference
  :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, RAPIDS, data science

.. _dask-hip:

********************************************************************
dask-hip documentation
********************************************************************

dask-hip is an extension of `Dask.distributed <https://distributed.dask.org/en/latest/>`_ for multi-GPU computing on AMD hardware. It is part of the AMD ROCm Data Science toolkit (ROCm-DS), an open-source software collection for high-performance data science applications. Forked from the `NVIDIA RAPIDS dask-cuda <https://github.com/rapidsai/dask-cuda>`_ project, dask-hip brings the same distributed GPU computing capabilities to the :doc:`HIP <hip:index>`/:doc:`ROCm <rocm:index>` stack while preserving API compatibility. For more information, see :doc:`What is dask-hip? <what-is-dask-hip>`

Key features include:

* **One GPU per worker** -- Automatically creates one Dask worker per available AMD GPU.
* **CPU affinity** -- Sets CPU affinity for each worker to optimize memory access locality.
* **UCX integration** -- High-performance communication via `UCX <https://www.openucx.org/>`_ with support for ROCm-IPC (GPU-to-GPU), InfiniBand, and TCP transports through `hipUCXX <https://github.com/AMD-AIOSS/hipUCXX>`_.
* **GPU memory spilling** -- Automatic spilling of GPU data to host memory when device memory is under pressure.
* **RMM memory pools** -- Integration with `RMM <https://github.com/rapidsai/rmm>`_ for efficient GPU memory management via pre-allocated pools.
* **Explicit communication** -- API for hand-tuned communication patterns that bypass the Dask scheduler.

The dask-hip code is open and hosted at `https://github.com/AMD-AIOSS/dask-hip <https://github.com/AMD-AIOSS/dask-hip>`_.

.. grid:: 2
  :gutter: 3

  .. grid-item-card:: Installation

    * :doc:`Installing dask-hip <install/install>`
    * :doc:`Building from source <install/build>`

  .. grid-item-card:: How to

    * :doc:`Quick start <how-to/quickstart>`
    * :doc:`UCX integration <how-to/ucx>`
    * :doc:`Spilling from device <how-to/spilling>`
    * :doc:`Explicit communication <how-to/explicit-comms>`

  .. grid-item-card:: API reference

    * :doc:`Python API reference <reference/api>`


To contribute to the documentation refer to `Contributing to ROCm-DS  <https://rocm.docs.amd.com/projects/rocm-ds/en/latest/contribute/contributing.html>`_.

You can find licensing information on the `Licensing <https://rocm.docs.amd.com/projects/rocm-ds/en/latest/about/license.html>`_ page.
