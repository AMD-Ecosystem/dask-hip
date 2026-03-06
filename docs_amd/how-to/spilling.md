<!-- SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc. -->
<!-- SPDX-License-Identifier: MIT -->

<head>
  <meta charset="UTF-8">
  <meta name="description" content="dask-hip GPU memory spilling guide">
  <meta name="keywords" content="Dask, GPU, memory, spilling, HIP, ROCm, ROCm-DS, AMD">
</head>

# Spilling from device

By default, dask-hip enables spilling from GPU to host memory when a GPU reaches a memory utilization of 80%. This can be changed to suit the needs of a workload, or disabled altogether, by explicitly setting `device_memory_limit`. This parameter accepts an integer or string memory size, or a float representing a percentage of the GPU's total memory:

```python
from dask_cuda import LocalCUDACluster

cluster = LocalCUDACluster(device_memory_limit=50000)  # spilling after 50000 bytes
cluster = LocalCUDACluster(device_memory_limit="5GB")   # spilling after 5 GB
cluster = LocalCUDACluster(device_memory_limit=0.3)     # spilling after 30% utilization
```

Memory spilling can be disabled by setting `device_memory_limit` to 0:

```python
cluster = LocalCUDACluster(device_memory_limit=0)  # spilling disabled
```

The same applies for `dask cuda worker`, where spilling can be controlled with `--device-memory-limit`:

```bash
$ dask scheduler
distributed.scheduler - INFO -   Scheduler at:  tcp://127.0.0.1:8786

$ dask cuda worker --device-memory-limit 5GB
$ dask cuda worker --device-memory-limit 0.3
$ dask cuda worker --device-memory-limit 0
```

## JIT-Unspill

The regular spilling in Dask and dask-hip has some significant limitations. Instead of tracking individual objects, it tracks task outputs. This means that a task returning a collection of GPU objects will either spill all of the objects or none of them. Other issues include object duplication, wrong spilling order, and non-tracking of shared device buffers.

dask-hip introduces JIT-Unspilling, which can improve performance and memory usage significantly. For workloads that require significant spilling (such as large joins on infrastructure with less available memory than data) improvements of greater than 50% have been observed.

To enable JIT-Unspilling, use the `jit_unspill` argument:

```python
from distributed import Client
from dask_cuda import LocalCUDACluster

cluster = LocalCUDACluster(n_workers=4, device_memory_limit="1GB", jit_unspill=True)
client = Client(cluster)
```

Or set the worker argument `--enable-jit-unspill`:

```bash
$ dask cuda worker --enable-jit-unspill
```

Or use the environment variable `DASK_JIT_UNSPILL=True`:

```bash
$ DASK_JIT_UNSPILL=True dask cuda worker
```

### Limitations

JIT-Unspill wraps GPU objects (such as `cudf.DataFrame`) in a `ProxyObject`. Objects proxied by a `ProxyObject` will be JIT-deserialized when accessed. The instance behaves as the proxied object and can be accessed just like the proxied object.

`ProxyObject` has some limitations and doesn't mimic the proxied object perfectly. Most notably, type checking using `isinstance()` works as expected but direct type checking doesn't:

```python
>>> import numpy as np
>>> from dask_cuda.proxy_object import asproxy
>>> x = np.arange(3)
>>> isinstance(asproxy(x), type(x))
True
>>> type(asproxy(x)) is type(x)
False
```

If encountering problems, use `unproxy()` to access the proxied object directly, or set `DASK_JIT_UNSPILL_COMPATIBILITY_MODE=True` to enable compatibility mode, which automatically calls `unproxy()` on all function inputs.

## cuDF spilling

When executing an ETL workflow with Dask cuDF (i.e., Dask DataFrame), it is usually best to leverage native spilling support in cuDF.

Native cuDF spilling has an important advantage over other methodologies: when JIT-unspill or default spilling are used, the worker is only able to spill the input or output of a task. When cuDF spilling is used, individual device buffers can be spilled and unspilled as needed while the task is executing.

When deploying a `LocalCUDACluster`, cuDF spilling can be enabled with the `enable_cudf_spill` argument:

```python
from distributed import Client
from dask_cuda import LocalCUDACluster

cluster = LocalCUDACluster(n_workers=4, enable_cudf_spill=True)
client = Client(cluster)
```

The same applies for `dask cuda worker`:

```bash
$ dask cuda worker --enable-cudf-spill
```

### cuDF spilling limitations

Although cuDF spilling is the best option for most ETL workflows using Dask cuDF, it will be much less effective if the workflow converts between `cudf.DataFrame` and other data formats (e.g., `cupy.ndarray`). Once the underlying device buffers are "exposed" to external memory references, they become "unspillable" by cuDF. In cases like this, JIT-Unspill is usually a better choice.
