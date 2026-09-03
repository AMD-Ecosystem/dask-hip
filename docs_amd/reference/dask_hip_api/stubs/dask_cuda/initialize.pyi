from _typeshed import Incomplete

from distributed.diagnostics.nvml import CudaDeviceInfo as CudaDeviceInfo

from .utils import (
    get_ucx_config as get_ucx_config,
    warn_about_nvlink_if_not_suppressed as warn_about_nvlink_if_not_suppressed,
)

logger: Incomplete
pre_existing_cuda_context: Incomplete
cuda_context_created: Incomplete

def initialize(
    create_cuda_context: bool = True,
    enable_tcp_over_ucx=None,
    enable_infiniband=None,
    enable_rocm_ipc=None,
    enable_rdmacm=None,
    enable_nvlink=None,
) -> None:
    """Create CUDA context and initialize UCXX configuration.

    Sometimes it is convenient to initialize the CUDA context, particularly before
    starting up Dask worker processes which create a variety of threads.

    To ensure UCX works correctly, it is important to ensure it is initialized with the
    correct options. This is especially important for the client, which cannot be
    configured to use UCX with arguments like ``LocalCUDACluster`` and
    ``dask cuda worker``. This function will ensure that they are provided a UCX
    configuration based on the flags and options passed by the user.

    This function can also be used as a worker preload so that Dask imports
    ``dask_cuda.initialize`` in each worker at startup. That applies UCX setup on
    workers that are not started through ``LocalCUDACluster`` or ``dask cuda worker``.

    You can add it to your global config with the following YAML:

    .. code-block:: yaml

        distributed:
          worker:
            preload:
              - dask_cuda.initialize

    Place this snippet in Dask's YAML config (for example ``~/.config/dask/``) or set
    the equivalent ``DASK_*`` environment variables so every worker preloads
    ``dask_cuda.initialize``.

    Parameters
    ----------
    create_cuda_context : bool, default True
        Create CUDA context on initialization.
    enable_tcp_over_ucx : bool, default None
        Set environment variables to enable TCP over UCX, even if InfiniBand and NVLink
        are not supported or disabled.
    enable_infiniband : bool, default None
        Set environment variables to enable UCX over InfiniBand, implies
        ``enable_tcp_over_ucx=True`` when ``True``.
    enable_rocm_ipc : bool, default None
        Set environment variables to enable UCX over ROCm-IPC, implies
        ``enable_tcp_over_ucx=True`` when ``True``.
    enable_rdmacm : bool, default None
        Set environment variables to enable UCX RDMA connection manager support,
        requires ``enable_infiniband=True``.
    enable_nvlink : bool, default None
        Unsupported on AMD, only provided for easy portability. Please use
        enable_rocm_ipc instead.
    """

def dask_setup(worker, create_cuda_context) -> None: ...
