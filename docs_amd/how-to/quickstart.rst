.. SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
.. SPDX-License-Identifier: MIT

.. meta::
   :description: dask-hip quick start guide
   :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, quickstart

.. _quickstart:

***********
Quick start
***********

A ``dask-hip`` cluster can be created using either ``LocalCUDACluster`` in Python or ``dask cuda worker`` from the command line.

.. note::

   As mentioned in :ref:`whatis-dask`, ``dask-hip`` retains dask-cuda API naming to minimize porting friction for developers working across both NVIDIA and AMD platforms.


LocalCUDACluster
================

To create a ``dask-hip`` cluster using all available GPUs and connect a Dask ``Client`` to it:

.. code-block:: python

   from dask_cuda import LocalCUDACluster
   from dask.distributed import Client

   cluster = LocalCUDACluster()
   client = Client(cluster)

.. tip::

   Be sure to include an ``if __name__ == "__main__":`` block when using ``LocalCUDACluster`` in a standalone Python script. See `standalone Python scripts <https://docs.dask.org/en/stable/scheduling.html#standalone-python-scripts>`_ for more details.

dask cuda worker
================

To create an equivalent cluster from the command line, ``dask-hip`` workers must be connected to a scheduler started with ``dask scheduler``:

.. code-block:: bash

   $ dask scheduler
   distributed.scheduler - INFO -   Scheduler at:  tcp://127.0.0.1:8786

   $ dask cuda worker 127.0.0.1:8786

To connect a client to this cluster:

.. code-block:: python

   from dask.distributed import Client

   client = Client("127.0.0.1:8786")

Selecting GPUs
==============

By default, ``dask-hip`` creates one worker for each visible GPU. You can control which GPUs are used via the ``HIP_VISIBLE_DEVICES`` environment variable:

.. code-block:: bash

   # Use only GPUs 0 and 2
   HIP_VISIBLE_DEVICES=0,2 dask cuda worker 127.0.0.1:8786

Or programmatically:

.. code-block:: python

   cluster = LocalCUDACluster(CUDA_VISIBLE_DEVICES="0,2")

.. note::

   Both ``HIP_VISIBLE_DEVICES`` and ``CUDA_VISIBLE_DEVICES`` are supported as environment variables. However, in code only ``CUDA_VISIBLE_DEVICES`` is supported.
