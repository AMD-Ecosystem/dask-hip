.. SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
.. SPDX-License-Identifier: MIT

.. meta::
   :description: dask-hip installation guide
   :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, install

.. _install:

*******************
Installing dask-hip
*******************

You can install ``dask-hip`` via AMD PyPI as described below. This is recommended for users of the package. For developers interested in modifying or contributing to the open-source ``dask-hip`` component, see the :doc:`Build instructions <build>`.

See :ref:`system-requirements` for information related to supported operating systems, ROCm versions, and AMD GPUs before installing ``dask-hip``.

Install dask-hip via AMD PyPI
==============================

Packaged versions of dask-hip and its dependencies are distributed via `AMD PyPI <https://pypi.amd.com/simple>`_. This section describes how to install dask-hip via this package index.

Create and activate a Conda environment with Python 3.12 as shown below:

.. code-block:: bash

   conda create --name dask-hip python=3.12
   conda activate dask-hip

dask-hip can then be installed into this environment using pip and the AMD PyPI URL:

.. code-block:: bash

   pip install amd-dask-hip --extra-index-url=https://pypi.amd.com/simple

hipUCXX support
---------------

To install the ``distributed-hipucxx`` package for high-performance UCX communication (ROCm-IPC, InfiniBand):

.. code-block:: bash

   pip install distributed-hipucxx --extra-index-url=https://pypi.amd.com/simple
