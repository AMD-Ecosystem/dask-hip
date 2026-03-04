# SPDX-FileCopyrightText: Copyright (c) 2019-2025, NVIDIA CORPORATION & AFFILIATES.
# SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: Apache-2.0 AND MIT

import sys

if sys.platform != "linux":
    raise ImportError("Only Linux is supported by Dask-CUDA at this time")


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

import dask
import dask.utils
from distributed.protocol.cuda import cuda_deserialize, cuda_serialize
from distributed.protocol.serialize import dask_deserialize, dask_serialize

from ._version import __git_commit__, __version__
from .cuda_worker import CUDAWorker
from .local_cuda_cluster import LocalCUDACluster

try:
    import dask.dataframe as dask_dataframe
except ImportError:
    # Dask DataFrame (optional) isn't installed
    dask_dataframe = None


if dask_dataframe is not None:
    from .explicit_comms.dataframe.shuffle import patch_shuffle_expression
    from .proxify_device_objects import proxify_decorator, unproxify_decorator

    # Monkey patching Dask to make use of explicit-comms when `DASK_EXPLICIT_COMMS=True`
    patch_shuffle_expression()
    # Monkey patching Dask to make use of proxify and unproxify in compatibility mode
    dask_dataframe.shuffle.shuffle_group = proxify_decorator(
        dask.dataframe.shuffle.shuffle_group
    )
    dask_dataframe.core._concat = unproxify_decorator(dask.dataframe.core._concat)

    def _register_cudf_spill_aware():
        import cudf

        # Only enable Dask/cuDF spilling if cuDF spilling is disabled, see
        # https://github.com/rapidsai/dask-cuda/issues/1363
        if not cudf.get_option("spill"):
            # This reproduces the implementation of `_register_cudf`, see
            # https://github.com/dask/distributed/blob/40fcd65e991382a956c3b879e438be1b100dff97/distributed/protocol/__init__.py#L106-L115
            from cudf.comm import serialize

    for registry in [
        cuda_serialize,
        cuda_deserialize,
        dask_serialize,
        dask_deserialize,
    ]:
        for lib in ["cudf", "dask_cudf"]:
            if lib in registry._lazy:
                registry._lazy[lib] = _register_cudf_spill_aware
