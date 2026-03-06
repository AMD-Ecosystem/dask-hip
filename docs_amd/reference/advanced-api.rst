.. SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
.. SPDX-License-Identifier: MIT

.. _dask-hip-advanced-api:

Advanced / Utility API
======================

GPU utilities
-------------

.. autoapifunction:: dask_cuda.utils.get_gpu_count

.. autoapifunction:: dask_cuda.utils.get_gpu_handle

.. autoapifunction:: dask_cuda.utils.get_gpu_uuid

.. autoapifunction:: dask_cuda.utils.get_n_gpus

.. autoapifunction:: dask_cuda.utils.get_device_total_memory

.. autoapifunction:: dask_cuda.utils.has_device_memory_resource

.. autoapifunction:: dask_cuda.utils.get_gpu_count_mig


CPU affinity
------------

.. autoapifunction:: dask_cuda.utils.get_cpu_affinity

.. autoapifunction:: dask_cuda.utils.get_cpu_count

.. autoapifunction:: dask_cuda.utils.unpack_bitmask


Device enumeration
------------------

.. autoapifunction:: dask_cuda.utils.cuda_visible_devices

.. autoapifunction:: dask_cuda.utils.nvml_device_index

.. autoapifunction:: dask_cuda.utils.parse_cuda_visible_device


Memory parsing
--------------

.. autoapifunction:: dask_cuda.utils.parse_device_bytes

.. autoapifunction:: dask_cuda.utils.parse_device_memory_limit

.. autoapifunction:: dask_cuda.utils.get_rmm_device_memory_usage


UCX configuration
-----------------

.. autoapifunction:: dask_cuda.utils.get_ucx_config

.. autoapifunction:: dask_cuda.utils.get_preload_options


Cluster introspection
---------------------

.. autoapifunction:: dask_cuda.utils.wait_workers

.. autoapifunction:: dask_cuda.utils.all_to_all

.. autoapifunction:: dask_cuda.utils.get_worker_config

.. autoapifunction:: dask_cuda.utils.get_cluster_configuration

.. autoapifunction:: dask_cuda.utils.print_cluster_config

.. autoapiclass:: dask_cuda.utils.CommaSeparatedChoice
   :members:
   :show-inheritance:


Worker plugins
--------------

.. autoapiclass:: dask_cuda.plugins.CPUAffinity
   :members:

.. autoapiclass:: dask_cuda.plugins.CUDFSetup
   :members:

.. autoapiclass:: dask_cuda.plugins.RMMSetup
   :members:

.. autoapiclass:: dask_cuda.plugins.PreImport
   :members:

.. autoapifunction:: dask_cuda.plugins.enable_rmm_memory_for_library


Proxy objects and JIT-Unspilling
--------------------------------

.. autoapifunction:: dask_cuda.proxy_object.asproxy

.. autoapiclass:: dask_cuda.proxy_object.ProxyObject
   :members:
   :undoc-members:

.. autoapifunction:: dask_cuda.proxify_device_objects.proxify_device_objects

.. autoapifunction:: dask_cuda.proxify_device_objects.unproxify_device_objects


Storage
-------

.. autoapiclass:: dask_cuda.device_host_file.DeviceHostFile
   :members:
   :undoc-members:

.. autoapiclass:: dask_cuda.device_host_file.LoggedBuffer
   :members:


RMM utilities
-------------

.. autoapifunction:: dask_cuda.utils.get_rmm_log_file_name


Explicit-comms helpers
----------------------

.. autoapifunction:: dask_cuda.explicit_comms.comms.worker_state

.. autoapifunction:: dask_cuda.explicit_comms.comms.pop_staging_area

.. autoapifunction:: dask_cuda.explicit_comms.dataframe.shuffle.patch_shuffle_expression
