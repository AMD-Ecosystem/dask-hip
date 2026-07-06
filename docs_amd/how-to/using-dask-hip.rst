.. meta::
   :description: Getting started with dask-hip for multi-GPU computing
   :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, tutorial, getting started

.. _using-dask-hip:

***************
Using dask-hip
***************

This topic walks through practical examples of GPU-distributed computing with
dask-hip, from creating a minimal cluster to deploying UCX-enabled multi-GPU
workloads. Complete example scripts are available in the ``examples/`` directory
of the repository.

.. note::

   dask-hip retains dask-cuda API naming (module ``dask_cuda``, command
   ``dask cuda worker``, class ``LocalCUDACluster``) to minimize porting
   friction for developers working across both ROCm and CUDA. See
   :ref:`whatis-dask` for more background.


Creating a cluster
==================

There are two ways to create a dask-hip cluster: programmatically in Python
or from the command line.

In a Python program:
--------------------

``LocalCUDACluster`` creates one Dask worker per visible GPU in the current
process. Connect a ``Client`` to submit work:

.. code-block:: python

   from dask_cuda import LocalCUDACluster
   from dask.distributed import Client

   if __name__ == "__main__":
       cluster = LocalCUDACluster()
       client = Client(cluster)

       # ... submit work ...

       client.shutdown()

.. tip::

   Always wrap ``LocalCUDACluster`` usage in an ``if __name__ == "__main__":``
   block when running as a standalone script. See
   `standalone Python scripts <https://docs.dask.org/en/stable/scheduling.html#standalone-python-scripts>`_
   for details.

From the command line:
----------------------

For multi-process deployments, start a scheduler and attach workers separately:

.. code-block:: bash

   $ dask scheduler
   distributed.scheduler - INFO -   Scheduler at:  tcp://127.0.0.1:8786

   $ dask cuda worker 127.0.0.1:8786

Then connect a client from Python:

.. code-block:: python

   from dask.distributed import Client

   client = Client("127.0.0.1:8786")

Selecting GPUs
--------------

By default, dask-hip creates one worker for each visible GPU. Control which
GPUs are used via the ``HIP_VISIBLE_DEVICES`` environment variable:

.. code-block:: bash

   HIP_VISIBLE_DEVICES=0,2 dask cuda worker 127.0.0.1:8786

Or programmatically:

.. code-block:: python

   cluster = LocalCUDACluster(HIP_VISIBLE_DEVICES="0,2")

.. note::

   Both ``HIP_VISIBLE_DEVICES`` and ``CUDA_VISIBLE_DEVICES`` are supported.


Basic GPU computation
=====================

The following example creates a cluster, generates a large random matrix on the
GPUs using `amd-cupy <https://pypi.amd.com/rocm-7.2.3/simple/amd-cupy/>`_ as the GPU
array backend, computes its sum across all GPUs, and collects the result:

.. code-block:: python

   from dask_cuda import LocalCUDACluster
   from dask.distributed import Client
   import dask.array as da
   import cupy

   if __name__ == "__main__":
       cluster = LocalCUDACluster()
       client = Client(cluster)

       # Create a 10000x10000 random matrix on the GPUs
       rs = da.random.RandomState(RandomState=cupy.random.RandomState)
       x = rs.random((10000, 10000), chunks=1000)

       # Compute the sum -- Dask distributes chunks across GPU workers
       result = x.sum().compute()
       print(f"Sum: {result}")

       client.shutdown()

Dask splits the array into chunks and distributes them across GPU workers. Each
chunk is backed by a ``cupy`` array in GPU memory. Operations like ``sum()`` are
executed in parallel on the GPUs, and Dask handles inter-worker communication
to combine partial results.


Using hipMM (RMM) memory pools
==============================

Pre-allocating a GPU memory pool with ``rmm_pool_size`` is recommended for
workloads that perform many allocations or use UCX communication. A pool avoids
repeated allocation overhead and, when using UCX, only requires a single IPC
handle registration for the entire pool rather than one per allocation:

.. code-block:: python

   cluster = LocalCUDACluster(rmm_pool_size="4GB")

Or from the command line:

.. code-block:: bash

   dask cuda worker 127.0.0.1:8786 --rmm-pool-size 4GB

For more on GPU memory management, see the ``device_memory_limit`` and
``jit_unspill`` parameters in the :doc:`API reference <../reference/api>`.


UCX-enabled local cluster
=========================

For high-performance GPU-to-GPU communication, dask-hip integrates with
`UCX <https://www.openucx.org/>`_ via
`hip-ucxx <https://github.com/ROCm-DS/hip-ucxx>`_. The following example
(from ``examples/ucx/local_cuda_cluster.py``) creates a UCX-enabled cluster
with ROCm-IPC transport:

.. code-block:: python

   from dask_cuda import LocalCUDACluster
   from dask.distributed import Client
   import dask.array as da
   import cupy

   if __name__ == "__main__":
       cluster = LocalCUDACluster(
           protocol="ucx",
           enable_tcp_over_ucx=True,
           enable_rocm_ipc=True,
           enable_infiniband=False,
           rmm_pool_size="1GB",
           interface="eth0",
       )
       client = Client(cluster)

       rs = da.random.RandomState(RandomState=cupy.random.RandomState)
       x = rs.random((10000, 10000), chunks=1000)
       x.sum().compute()

       client.shutdown()

Key options:

- ``enable_rocm_ipc`` -- enables GPU-to-GPU transfers via ROCm-IPC (intra-node)
- ``enable_infiniband`` -- enables InfiniBand RDMA transfers (inter-node)
- ``enable_rdmacm`` -- enables the RDMA connection manager (recommended with InfiniBand)
- ``interface`` -- network interface for the scheduler; required when ROCm-IPC or InfiniBand are enabled
- ``rmm_pool_size`` -- pre-allocates a hipMM (RMM) memory pool per worker

For the full range of UCX configuration options, see the ``LocalCUDACluster``
and ``CUDAWorker`` parameters in the :doc:`API reference <../reference/api>`.


Multi-process deployment with UCX
=================================

In production, the scheduler, workers, and client typically run as separate
processes. The ``examples/ucx/`` directory demonstrates this pattern.

Step 1: Launch scheduler and workers
-------------------------------------

Use ``dask cuda worker`` with UCX flags, or the provided
``examples/ucx/dask_cuda_worker.sh`` script:

.. code-block:: bash

   # Start the scheduler with UCX protocol
   dask scheduler --protocol ucx --scheduler-file scheduler.json &

   # Attach GPU workers with ROCm-IPC and a memory pool
   dask cuda worker --scheduler-file scheduler.json \
       --enable-tcp-over-ucx \
       --enable-rocm-ipc \
       --rmm-pool-size 1GB

Or use the helper script which handles environment variables and flags:

.. code-block:: bash

   bash examples/ucx/dask_cuda_worker.sh -i eth0 -t rocm-ipc -r 2GB

Step 2: Connect a client
-------------------------

From a separate process, use ``initialize()`` to configure UCX on the client
side before connecting (from ``examples/ucx/client_initialize.py``):

.. code-block:: python

   from dask.distributed import Client
   from dask_cuda.initialize import initialize
   import dask.array as da
   import cupy

   if __name__ == "__main__":
       initialize(
           enable_tcp_over_ucx=True,
           enable_rocm_ipc=True,
       )

       client = Client("ucx://127.0.0.1:8786")

       rs = da.random.RandomState(RandomState=cupy.random.RandomState)
       x = rs.random((10000, 10000), chunks=1000)
       x.sum().compute()

       client.shutdown()

The ``initialize()`` call configures Dask UCX settings so the client can
communicate with the scheduler and workers using the same transports.
