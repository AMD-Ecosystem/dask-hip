from _typeshed import Incomplete

from distributed import LocalCluster, Nanny, Worker

from .initialize import initialize as initialize
from .utils import (
    cuda_visible_devices as cuda_visible_devices,
    get_ucx_config as get_ucx_config,
    nvml_device_index as nvml_device_index,
    parse_cuda_visible_device as parse_cuda_visible_device,
    parse_device_memory_limit as parse_device_memory_limit,
    warn_about_nvlink_if_not_suppressed as warn_about_nvlink_if_not_suppressed,
)
from .worker_common import (
    worker_data_function as worker_data_function,
    worker_plugins as worker_plugins,
)

class LoggedWorker(Worker):
    def __init__(self, *args, **kwargs) -> None: ...
    async def start(self) -> None: ...

class LoggedNanny(Nanny):
    def __init__(self, *args, **kwargs) -> None: ...

class LocalCUDACluster(LocalCluster):
    """A variant of ``dask.distributed.LocalCluster`` that uses one GPU per process.

    This assigns a different ``CUDA_VISIBLE_DEVICES`` environment variable to each Dask
    worker process.

    For machines with a complex architecture mapping CPUs, GPUs, and network hardware,
    such as NVIDIA DGX-1 and DGX-2, this class creates a local cluster that tries to
    respect this hardware as much as possible.

    Each worker process is automatically assigned the correct CPU cores and network
    interface cards to maximize performance. If UCX and distributed-ucxx are available,
    InfiniBand and NVLink connections can be used to optimize data transfer performance.

    Parameters
    ----------
    CUDA_VISIBLE_DEVICES : str, list of int, or None, default None
        GPUs to restrict activity to. Can be a string (like ``"0,1,2,3"``), list (like
        ``[0, 1, 2, 3]``), or ``None`` to use all available GPUs.
    n_workers : int or None, default None
        Number of workers. Can be an integer or ``None`` to fall back on the GPUs
        specified by ``CUDA_VISIBLE_DEVICES``. The value of ``n_workers`` must be
        smaller or equal to the number of GPUs specified in ``CUDA_VISIBLE_DEVICES``
        when the latter is specified, and if smaller, only the first ``n_workers`` GPUs
        will be used.
    threads_per_worker : int, default 1
        Number of threads to be used for each Dask worker process.
    memory_limit : int, float, str, or None, default "auto"
        Size of the host LRU cache, which is used to determine when the worker
        starts spilling to disk (not available if JIT-Unspill is enabled). Can be an
        integer (bytes), float (fraction of total system memory), string (like ``"5GB"``
        or ``"5000M"``), or ``"auto"``, 0, or ``None`` for no memory management.
    device_memory_limit : int, float, str, or None, default "default"
        Size of the CUDA device LRU cache, which is used to determine when the worker
        starts spilling to host memory. Can be an integer (bytes), float (fraction of
        total device memory), string (like ``"5GB"`` or ``"5000M"``), ``"auto"``, ``0``
        or ``None`` to disable spilling to host (i.e. allow full device memory usage).
        Another special value ``"default"`` (which happens to be the default) is also
        available and uses the recommended Dask-CUDA\'s defaults and means 80% of the
        total device memory (analogous to ``0.8``), and disabled spilling (analogous
        to ``auto``/``0``) on devices without a dedicated memory resource, such as
        system on a chip (SoC) devices.
    enable_cudf_spill : bool, default False
        Enable automatic cuDF spilling.

        .. warning::
            This should NOT be used together with JIT-Unspill.
    cudf_spill_stats : int, default 0
        Set the cuDF spilling statistics level. This option has no effect if
        ``enable_cudf_spill=False``.
    local_directory : str or None, default None
        Path on local machine to store temporary files. Can be a string (like
        ``"path/to/files"``) or ``None`` to fall back on the value of
        ``dask.temporary-directory`` in the local Dask configuration, using the current
        working directory if this is not set.
    shared_filesystem: bool or None, default None
        Whether the ``local_directory`` above is shared between all workers or not.
        If ``None``, the "jit-unspill-shared-fs" config value are used, which
        defaults to True. Notice, in all other cases this option defaults to False,
        but on a local cluster it defaults to True -- we assume all workers use the
        same filesystem.
    protocol : str or None, default None
        Protocol to use for communication. Can be a string (like ``"tcp"`` or
        ``"ucx"``), or ``None`` to automatically choose the correct protocol.
    enable_tcp_over_ucx : bool, default None
        Set environment variables to enable TCP over UCX, even if InfiniBand and NVLink
        are not supported or disabled.
    enable_infiniband : bool, default None
        Set environment variables to enable UCX over InfiniBand, requires
        ``protocol="ucx"``, and implies ``enable_tcp_over_ucx=True`` when ``True``.
    enable_rocm_ipc : bool, default None
        Set environment variables to enable UCX over ROCm-IPC, requires
        ``protocol="ucx"``, and implies ``enable_tcp_over_ucx=True`` when ``True``.
    enable_rdmacm : bool, default None
        Set environment variables to enable UCX RDMA connection manager support,
        requires ``protocol="ucx"``, and ``enable_infiniband=True``.
    rmm_pool_size : int, str or None, default None
        RMM pool size to initialize each worker with. Can be an integer (bytes), float
        (fraction of total device memory), string (like ``"5GB"`` or ``"5000M"``), or
        ``None`` to disable RMM pools.

        .. note::
            This size is a per-worker configuration, and not cluster-wide.
    rmm_maximum_pool_size : int, str or None, default None
        When ``rmm_pool_size`` is set, this argument indicates
        the maximum pool size.
        Can be an integer (bytes), float (fraction of total device memory), string
        (like ``"5GB"`` or ``"5000M"``) or ``None``. By default, the total available
        memory on the GPU is used. ``rmm_pool_size`` must be specified to use RMM pool
        and to set the maximum pool size.

        .. note::
            When paired with ``--enable-rmm-async`` the maximum size cannot be
            guaranteed due to fragmentation.

        .. note::
            This size is a per-worker configuration, and not cluster-wide.
    rmm_managed_memory : bool, default False
        Initialize each worker with RMM and set it to use managed memory. If disabled,
        RMM may still be used by specifying ``rmm_pool_size``.

        .. warning::
            Managed memory is currently incompatible with NVLink. Trying to enable both
            will result in an exception.
    rmm_async: bool, default False
        Initialize each worker with RMM and set it to use RMM\'s asynchronous allocator.
        See ``rmm.mr.CudaAsyncMemoryResource`` for more info.

        .. warning::
            The asynchronous allocator is incompatible with RMM pools and managed
            memory. Trying to enable both will result in an exception.
    rmm_allocator_external_lib_list: str, list or None, default None
        List of external libraries for which to set RMM as the allocator.
        Supported options are: ``["torch", "cupy"]``. Can be a comma-separated string
        (like ``"torch,cupy"``) or a list of strings (like ``["torch", "cupy"]``).
        If ``None``, no external libraries will use RMM as their allocator.
    rmm_release_threshold: int, str or None, default None
        When ``rmm.async is True`` and the pool size grows beyond this value, unused
        memory held by the pool will be released at the next synchronization point.
        Can be an integer (bytes), float (fraction of total device memory), string (like
        ``"5GB"`` or ``"5000M"``) or ``None``. By default, this feature is disabled.

        .. note::
            This size is a per-worker configuration, and not cluster-wide.
    rmm_log_directory : str or None, default None
        Directory to write per-worker RMM log files to. The client and scheduler are not
        logged here. Can be a string (like ``"/path/to/logs/"``) or ``None`` to
        disable logging.

        .. note::
            Logging will only be enabled if ``rmm_pool_size`` is specified or
            ``rmm_managed_memory=True``.
    rmm_track_allocations : bool, default False
        If True, wraps the memory resource used by each worker with a
        ``rmm.mr.TrackingResourceAdaptor``, which tracks the amount of
        memory allocated.

        .. note::
             This option enables additional diagnostics to be collected and
             reported by the Dask dashboard. However, there is significant overhead
             associated with this and it should only be used for debugging and
             memory profiling.
    jit_unspill : bool or None, default None
        Enable just-in-time unspilling. Can be a boolean or ``None`` to fall back on
        the value of ``dask.jit-unspill`` in the local Dask configuration, disabling
        unspilling if this is not set.

        .. note::
            This is experimental and doesn\'t support memory spilling to disk. See
            ``proxy_object.ProxyObject`` and ``proxify_host_file.ProxifyHostFile`` for
            more info.
    log_spilling : bool, default True
        Enable logging of spilling operations directly to ``distributed.Worker`` with an
        ``INFO`` log level.
    pre_import : str, list or None, default None
        Pre-import libraries as a Worker plugin to prevent long import times bleeding
        through later Dask operations. Should be a list of comma-separated names,
        such as "cudf,rmm" or a list of strings such as ["cudf", "rmm"].

    Examples
    --------
    >>> from dask_cuda import LocalCUDACluster
    >>> from dask.distributed import Client
    >>> cluster = LocalCUDACluster()
    >>> client = Client(cluster)

    Raises
    ------
    TypeError
        If InfiniBand or NVLink are enabled and ``protocol != "ucx"``.
    ValueError
        If RMM pool, RMM managed memory or RMM async allocator are requested but RMM
        cannot be imported.
        If RMM managed memory and asynchronous allocator are both enabled.
        If RMM maximum pool size is set but RMM pool size is not.
        If RMM maximum pool size is set but RMM async allocator is used.
        If RMM release threshold is set but the RMM async allocator is not being used.

    See Also
    --------
    LocalCluster
    """

    memory_limit: Incomplete
    device_memory_limit: Incomplete
    enable_cudf_spill: Incomplete
    cudf_spill_stats: Incomplete
    rmm_pool_size: Incomplete
    rmm_maximum_pool_size: Incomplete
    rmm_managed_memory: Incomplete
    rmm_async: Incomplete
    rmm_release_threshold: Incomplete
    rmm_allocator_external_lib_list: Incomplete
    rmm_log_directory: Incomplete
    rmm_track_allocations: Incomplete
    data: Incomplete
    host: Incomplete
    pre_import: Incomplete
    cuda_visible_devices: Incomplete
    def __init__(
        self,
        CUDA_VISIBLE_DEVICES=None,
        n_workers=None,
        threads_per_worker: int = 1,
        memory_limit: str = "auto",
        device_memory_limit: str = "default",
        enable_cudf_spill: bool = False,
        cudf_spill_stats: int = 0,
        local_directory=None,
        shared_filesystem=None,
        protocol=None,
        enable_tcp_over_ucx=None,
        enable_infiniband=None,
        enable_rocm_ipc=None,
        enable_rdmacm=None,
        rmm_pool_size=None,
        rmm_maximum_pool_size=None,
        rmm_managed_memory: bool = False,
        rmm_async: bool = False,
        rmm_allocator_external_lib_list=None,
        rmm_release_threshold=None,
        rmm_log_directory=None,
        rmm_track_allocations: bool = False,
        jit_unspill=None,
        log_spilling: bool = False,
        pre_import=None,
        enable_nvlink=None,
        **kwargs
    ) -> None: ...
    def new_worker_spec(self): ...
