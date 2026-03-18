.. meta::
  :description: dask-hip documentation and API reference
  :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, RAPIDS, data science

.. _whatis-dask:

*****************
What is dask-hip?
*****************

Dask-HIP is an extension of `Dask.distributed <https://distributed.dask.org/en/latest/>`__ that simplifies deploying Dask clusters on multi-GPU systems. ``dask-hip`` is part of the AMD ROCm Data Science toolkit (ROCm-DS) and works alongside other ROCm-DS components such as `hipDF <https://github.com/AMD-AIOSS/hipDF>`__, `hipRaft <https://github.com/AMD-AIOSS/hipRaft>`__, and `hipUCXX <https://github.com/AMD-AIOSS/hipUCXX>`__.

``dask-hip`` has been adapted from `dask-cuda <https://github.com/rapidsai/dask-cuda>`__ from the RAPIDS project by NVIDIA for the HIP/ROCm stack. It preserves the directory structure, file naming, and API naming to minimize porting friction for developers working across both NVIDIA and AMD platforms. 

Key capabilities include:

- **One worker per GPU** with automatic ``HIP_VISIBLE_DEVICES`` management
- **CPU affinity** for each worker, optimizing memory locality
- **UCX communication** for high-performance networking (GPU-direct, InfiniBand, TCP)
- **GPU memory spilling** to host memory at configurable thresholds
- **RMM pool integration** for pre-allocated GPU memory pools
- **Explicit communication API** for hand-tuned computation and communication patterns
- **CLI tools** (``dask cuda worker``) for deploying GPU workers from the command line

Differences with dask-cuda
==========================

The following summarizes the main adaptations made for the AMD platform:

.. list-table::
   :header-rows: 1

   * - Feature
     - ``dask-cuda``
     - ``dask-hip``

   * - GPU runtime
     - CUDA
     - HIP

   * - GPU-to-GPU transport
     - NVLink (``cuda_ipc``)
     - ROCm-IPC (``rocm_ipc``)

   * - GPU copy transport
     - ``cuda_copy``
     - ``rocm_copy``

   * - GPU management library
     - ``pynvml`` (nvidia-ml-py)
     - ``amdsmi`` (via ``pynvml2amdsmi`` shim)

   * - Numba backend
     - ``numba.cuda``
     - ``numba.hip``

   * - CUDA context creation
     - ``cuda.core.experimental``
     - ``hip.hip.hipSetDevice``

   * - Communication library
     - UCXX
     - hipUCXX

   * - Package name
     - ``dask-cuda``
     - ``amd-dask-hip``

pynvml compatibility shim
-------------------------

dask-hip includes a ``pynvml2amdsmi`` compatibility layer that maps ``pynvml`` API calls to their AMD SMI equivalents. This allows upstream code that depends on ``pynvml`` (such as ``distributed.diagnostics.nvml``) to work transparently on AMD hardware without modification.

NVLink backward compatibility
-----------------------------

For portability, dask-hip accepts ``enable_nvlink`` parameters and ``--enable-nvlink`` CLI flags, mapping them to ``enable_rocm_ipc`` / ``--enable-rocm-ipc`` with a deprecation warning. This can be suppressed by setting the ``DASK_HIP_SUPPRESS_NVLINK_WARNING=1`` environment variable.
