<!-- SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc. -->
<!-- SPDX-License-Identifier: MIT -->

Dask HIP
=========

Various utilities to improve deployment and management of Dask workers on
HIP-enabled systems.

This library is experimental, and its API is subject to change at any time
without notice.

Example
-------

```python
from dask_cuda import LocalCUDACluster
from dask.distributed import Client

cluster = LocalCUDACluster()
client = Client(cluster)
```

Documentation is available [here](https://rocm.docs.amd.com/projects/dask-hip-internal/en/dev-suphilip-add_amd_documentation/).
