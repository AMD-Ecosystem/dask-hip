.. SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
.. SPDX-License-Identifier: MIT

.. _dask-hip-core-api:

Core API
========

Cluster management
------------------

.. autoapiclass:: dask_cuda.local_cuda_cluster.LocalCUDACluster
   :members:
   :undoc-members:
   :show-inheritance:

Worker
------

.. autoapiclass:: dask_cuda.cuda_worker.CUDAWorker
   :members:
   :undoc-members:
   :show-inheritance:

Worker specification
--------------------

.. autoapifunction:: dask_cuda.worker_spec.worker_spec

Client initialization
---------------------

.. autoapifunction:: dask_cuda.initialize.initialize


Explicit communication
----------------------

.. autoapiclass:: dask_cuda.explicit_comms.comms.CommsContext
   :members:
   :undoc-members:

.. autoapifunction:: dask_cuda.explicit_comms.comms.default_comms

.. autoapifunction:: dask_cuda.explicit_comms.dataframe.shuffle.shuffle


CLI
---

dask-cuda-worker
~~~~~~~~~~~~~~~~

.. include:: dask_cuda_api/stubs/cli_worker.rst

dask-cuda-config
~~~~~~~~~~~~~~~~

.. include:: dask_cuda_api/stubs/cli_config.rst
