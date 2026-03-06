<!-- SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc. -->
<!-- SPDX-License-Identifier: MIT -->

# What is dask-hip?

## Overview

Dask-CUDA is an extension of [Dask.distributed](https://distributed.dask.org/en/latest/) that simplifies deploying Dask clusters on multi-GPU systems. It automatically creates one Dask worker per GPU, configures CPU affinity for optimal memory access, and integrates with high-performance communication frameworks like [UCX](https://www.openucx.org/) for GPU-to-GPU and InfiniBand transfers. It also provides GPU memory spilling when device memory is under pressure and supports [RMM](https://github.com/rapidsai/rmm) memory pools for efficient allocation.

Key capabilities include:

- **One worker per GPU** with automatic `CUDA_VISIBLE_DEVICES` management
- **CPU affinity** for each worker, optimizing memory locality
- **UCX communication** for high-performance networking (GPU-direct, InfiniBand, TCP)
- **GPU memory spilling** to host memory at configurable thresholds
- **RMM pool integration** for pre-allocated GPU memory pools
- **Explicit communication API** for hand-tuned computation and communication patterns
- **CLI tools** (`dask cuda worker`) for deploying GPU workers from the command line

## AMD ROCm port

dask-hip is AMD's ROCm-native port of the [NVIDIA RAPIDS dask-cuda](https://github.com/rapidsai/dask-cuda) project. It has been adapted for the HIP/ROCm stack while preserving the directory structure, file naming, and API naming to minimize porting friction for developers working across both NVIDIA and AMD platforms. dask-hip is part of the AMD ROCm Data Science toolkit (ROCm-DS) and works alongside other ROCm-DS components such as [hipDF](https://github.com/AMD-AIOSS/hipDF), [hipRaft](https://github.com/AMD-AIOSS/hipRaft), and [hipUCXX](https://github.com/AMD-AIOSS/hipUCXX).

## Key differences from dask-cuda

The following summarizes the main adaptations made for the AMD platform:

| Area | dask-cuda (NVIDIA) | dask-hip (AMD) |
|------|-------------------|----------------|
| GPU runtime | CUDA | HIP/ROCm |
| GPU-to-GPU transport | NVLink (`cuda_ipc`) | ROCm-IPC (`rocm_ipc`) |
| GPU copy transport | `cuda_copy` | `rocm_copy` |
| GPU management library | `pynvml` (nvidia-ml-py) | `amdsmi` (via `pynvml2amdsmi` shim) |
| Numba backend | `numba.cuda` | `numba.hip` |
| CUDA context creation | `cuda.core.experimental` | `hip.hip.hipSetDevice` |
| Communication library | UCXX | hipUCXX |
| Package name | `dask-cuda` | `amd-dask-hip` |

### pynvml compatibility shim

dask-hip includes a `pynvml2amdsmi` compatibility layer that maps pynvml API calls to their AMD SMI equivalents. This allows upstream code that depends on `pynvml` (such as `distributed.diagnostics.nvml`) to work transparently on AMD hardware without modification.

### NVLink backward compatibility

For portability, dask-hip accepts `enable_nvlink` parameters and `--enable-nvlink` CLI flags, mapping them to `enable_rocm_ipc` / `--enable-rocm-ipc` with a deprecation warning. This can be suppressed by setting the `DASK_HIP_SUPPRESS_NVLINK_WARNING=1` environment variable.
