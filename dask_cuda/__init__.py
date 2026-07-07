# SPDX-FileCopyrightText: Copyright (c) 2019-2026, NVIDIA CORPORATION. All rights reserved.
# SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: Apache-2.0 AND MIT

import sys

if sys.platform != "linux":
    raise ImportError("Only Linux is supported by Dask-HIP at this time")

def __init_dask_cuda_rocm():
    import os
    import shutil

    # Check if ROCm is available and perform initialization, silently move on
    # if ROCm is not found
    has_amdgpu = os.path.exists("/dev/kfd") and os.path.exists("/dev/dri")
    if not has_amdgpu:
        return False

    cmd = "amd-smi"
    cmd_path = shutil.which(cmd)
    if not cmd_path:
        return False

    # set HIP_VISIBLE_DEVICES as CUDA_VISIBLE_DEVICES if the latter is not set
    if "HIP_VISIBLE_DEVICES" in os.environ and "CUDA_VISIBLE_DEVICES" not in os.environ:
        os.environ["CUDA_VISIBLE_DEVICES"] = os.environ["HIP_VISIBLE_DEVICES"]

    return True


DASK_USE_ROCM = __init_dask_cuda_rocm()


from distributed.protocol.cuda import cuda_deserialize, cuda_serialize
from distributed.protocol.serialize import dask_deserialize, dask_serialize

from ._version import __git_commit__, __version__
from .cuda_worker import CUDAWorker

from .local_cuda_cluster import LocalCUDACluster

def _register_cudf_spill_aware():
    """Lazy hook for Distributed; no-op if hipDF is not installed."""
    try:
        import cudf
    except ImportError:
        return

    # Only enable Dask/cuDF spilling if cuDF spilling is disabled, see
    # https://github.com/rapidsai/dask-cuda/issues/1363
    if not cudf.get_option("spill"):
        # This reproduces the implementation of `_register_cudf`, see
        # https://github.com/dask/distributed/blob/40fcd65e991382a956c3b879e438be1b100dff97/distributed/protocol/__init__.py#L106-L115
        from cudf.comm import serialize  # noqa: F401


for registry in [
    cuda_serialize,
    cuda_deserialize,
    dask_serialize,
    dask_deserialize,
]:
    for lib in ["cudf", "dask_cudf"]:
        if lib in registry._lazy:
            registry._lazy[lib] = _register_cudf_spill_aware
