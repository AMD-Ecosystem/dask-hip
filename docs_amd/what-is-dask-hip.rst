.. meta::
  :description: dask-hip documentation and API reference
  :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, RAPIDS, AMD Data Science

.. _whatis-dask:

*****************
What is dask-hip?
*****************

dask-hip is an extension of `Dask.distributed <https://distributed.dask.org/en/latest/>`__ that
simplifies the deployment of Dask clusters on multi-GPU systems. dask-hip is part of the AMD Data
Science toolkit (ROCm-DS) and works alongside other ROCm-DS components such as
`hipDF <https://github.com/AMD-Ecosystem/hipDF>`__, `hipRAFT <https://github.com/AMD-Ecosystem/hipRaft>`__,
and `hip-ucxx <https://github.com/AMD-Ecosystem/hip-ucxx>`__.

dask-hip has been adapted from dask-cuda part of the RAPIDS project. It preserves the directory structure, file naming,
and API naming to minimize porting friction for developers migrating their workloads to AMD platforms.

Key capabilities include:

- **One worker per GPU** with automatic ``HIP_VISIBLE_DEVICES`` management
- **CPU affinity** for each worker, optimizing memory locality
- **UCX communication** for high-performance networking (GPU-direct, InfiniBand, TCP)
- **GPU memory spilling** to host memory at configurable thresholds
- **hipMM (RMM) pool integration** for pre-allocated GPU memory pools
- **Explicit communication API** for hand-tuned computation and communication patterns
- **CLI tools** (``dask cuda worker``) for deploying GPU workers from the command line
