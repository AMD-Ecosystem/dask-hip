<!-- SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc. -->
<!-- SPDX-License-Identifier: MIT -->

<head>
  <meta charset="UTF-8">
  <meta name="description" content="dask-hip UCX integration guide">
  <meta name="keywords" content="Dask, GPU, UCX, ROCm-IPC, InfiniBand, RDMA, HIP, ROCm, ROCm-DS, AMD">
</head>

# UCX integration

Communication can be a major bottleneck in distributed systems. dask-hip addresses this by supporting integration with [UCX](https://www.openucx.org/), an optimized communication framework that provides high-performance networking and supports a variety of transport methods, including ROCm-IPC for GPU-to-GPU transfers, [InfiniBand](https://www.mellanox.com/pdf/whitepapers/IB_Intro_WP_190.pdf) for systems with specialized hardware, and TCP for systems without it. This integration is enabled through [hipUCXX](https://github.com/AMD-AIOSS/hipUCXX), which provides Python bindings for UCX on AMD GPUs.

## Hardware requirements

To use UCX with ROCm-IPC or InfiniBand, relevant GPUs must be connected via AMD Infinity Fabric / XGMI links or InfiniBand adapters, respectively.

## Software requirements

UCX integration requires an environment with both UCX and hipUCXX installed; see [Installing dask-hip](../install/install.md) for detailed instructions.

When using UCX, each GPU memory buffer must create a mapping between each unique pair of processes it is transferred across; this can be quite costly. For this reason, it is strongly recommended to use [RMM](https://github.com/rapidsai/rmm) to allocate a memory pool that is only prone to a single mapping operation.

```{warning}
dask-hip must create worker GPU contexts during cluster initialization, and properly ordering that task is critical for correct UCX configuration. If a GPU context already exists for this process at the time of cluster initialization, unexpected behavior can occur. To avoid this, initialize any UCX-enabled clusters before doing operations that would result in a GPU context being created.

For some ROCm-DS libraries (e.g., hipDF), setting `RAPIDS_NO_INITIALIZE=1` at runtime will delay or disable their GPU context creation.
```

## Configuration

UCX configuration can be provided via:

1. **YAML configuration files**: `distributed-ucxx.yaml`
2. **Environment variables**: Using the `DASK_DISTRIBUTED_UCXX_` prefix
3. **Programmatic configuration**: Using Dask's configuration system

### Example configuration

```yaml
distributed-ucxx:
  tcp: true
  rocm-ipc: true
  infiniband: false
  rocm-copy: true
  create-cuda-context: true
  rmm:
    pool-size: "1GB"
```

### Environment variables

```bash
export DASK_DISTRIBUTED_UCXX__TCP=true
export DASK_DISTRIBUTED_UCXX__ROCM_IPC=true
export DASK_DISTRIBUTED_UCXX__RMM__POOL_SIZE=1GB
```

### Python configuration

```python
import dask

dask.config.set({
    "distributed-ucxx.tcp": True,
    "distributed-ucxx.rocm-ipc": True,
    "distributed-ucxx.rmm.pool-size": "1GB"
})
```

## Configuration types

### Automatic

Specifying UCX transports is optional. A local cluster can be started with `LocalCUDACluster(protocol="ucx")`, implying automatic UCX transport selection (`UCX_TLS=all`).

Starting a cluster separately (scheduler, workers, and client as different processes) is also possible, as long as the Dask scheduler is created with `dask scheduler --protocol="ucx"` and connecting a `dask cuda worker` to the scheduler will imply automatic UCX transport selection, but that requires the Dask scheduler and client to be started with `DASK_DISTRIBUTED_UCXX__CREATE_CUDA_CONTEXT=True`.

### Manual

For manual configuration, several options must be specified within your Dask configuration to enable the integration. These affect `UCX_TLS` and `UCX_SOCKADDR_TLS_PRIORITY`, environment variables used by UCX to decide what transport methods to use and which to prioritize:

- `distributed-ucxx.rocm-copy: true` -- **required.** Adds `rocm_copy` to `UCX_TLS`, enabling GPU transfers over UCX.

- `distributed-ucxx.tcp: true` -- **required.** Adds `tcp` to `UCX_TLS`, enabling TCP transfers over UCX; this is required for very small transfers which are inefficient for ROCm-IPC and InfiniBand.

- `distributed-ucxx.rocm-ipc: true` -- **required for ROCm-IPC.** Adds `rocm_ipc` to `UCX_TLS`, enabling GPU-to-GPU transfers over UCX; affects intra-node communication only.

- `distributed-ucxx.infiniband: true` -- **required for InfiniBand.** Adds `rc` to `UCX_TLS`, enabling InfiniBand transfers over UCX.

- `distributed-ucxx.rdmacm: true` -- **recommended for InfiniBand.** Replaces `sockcm` with `rdmacm` in `UCX_SOCKADDR_TLS_PRIORITY`, enabling remote direct memory access (RDMA) for InfiniBand transfers.

- `distributed-ucxx.rmm.pool-size: <str|int>` -- **recommended.** Allocates an RMM pool of the specified size for the process; size can be provided with an integer number of bytes or in human-readable format, e.g., `"4GB"`.

## Usage examples

### LocalCUDACluster with UCX

```python
from dask_cuda import LocalCUDACluster
from dask.distributed import Client

cluster = LocalCUDACluster(
    protocol="ucx",
    enable_rocm_ipc=True,
    enable_infiniband=False,
    rmm_pool_size="1GB",
)
client = Client(cluster)
```

### dask cuda worker with UCX

```bash
dask scheduler --protocol="ucx"

dask cuda worker ucx://127.0.0.1:8786 \
    --enable-rocm-ipc \
    --rmm-pool-size="1GB"
```

## Running in a fork-starved environment

Many high-performance networking stacks do not support calling `fork()` after the network substrate is initialized. To mitigate this when using dask-hip's UCX integration, use the `"forkserver"` multiprocessing method. When launching workers using `dask cuda worker`, pass `--multiprocessing-method forkserver`. In user code:

```python
import dask

if __name__ == "__main__":
    import multiprocessing.forkserver as f
    f.ensure_running()
    with dask.config.set(
        {"distributed.worker.multiprocessing-method": "forkserver"}
    ):
        run_analysis(...)
```

## Troubleshooting

### Timeouts

Depending on the cluster size and GPU architecture, timeouts may occur when establishing endpoints between Dask workers. Increase the default timeout via the `distributed-ucxx.connect-timeout` configuration or the `DASK_DISTRIBUTED_UCXX__CONNECT_TIMEOUT` environment variable. The value represents the timeout in seconds.
