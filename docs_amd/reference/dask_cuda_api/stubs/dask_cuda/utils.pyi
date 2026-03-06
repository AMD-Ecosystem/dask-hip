from contextlib import contextmanager
from functools import singledispatch

import click
import toolz

def unpack_bitmask(x, mask_bits: int = 64):
    """Unpack a list of integers containing bitmasks.

    Parameters
    ----------
    x: list of int
        A list of integers
    mask_bits: int
        An integer determining the bitwidth of ``x``

    Examples
    --------
    >>> from dask_cuda.utils import unpack_bitmaps
    >>> unpack_bitmask([1 + 2 + 8])
    [0, 1, 3]
    >>> unpack_bitmask([1 + 2 + 16])
    [0, 1, 4]
    >>> unpack_bitmask([1 + 2 + 16, 2 + 4])
    [0, 1, 4, 65, 66]
    >>> unpack_bitmask([1 + 2 + 16, 2 + 4], mask_bits=32)
    [0, 1, 4, 33, 34]
    """

@toolz.memoize
def get_cpu_count(): ...
@toolz.memoize
def get_gpu_count(): ...
def get_gpu_handle(device_id: int = 0):
    """Get GPU handle from device index or UUID.

    Parameters
    ----------
    device_id: int or str
        The index or UUID of the device from which to obtain the handle.

    Raises
    ------
    ValueError
        If acquiring the device handle for the device specified failed.
    pynvml.NVMLError
        If any NVML error occurred while initializing.

    Examples
    --------
    >>> get_gpu_handle(device_id=0)

    >>> get_gpu_handle(device_id="GPU-9fb42d6f-7d6b-368f-f79c-3c3e784c93f6")
    """

@toolz.memoize
def get_gpu_count_mig(return_uuids: bool = False):
    """Return the number of MIG instances available

    Parameters
    ----------
    return_uuids: bool
        Returns the uuids of the MIG instances available optionally

    """

def get_cpu_affinity(device_index=None):
    """Get a list containing the CPU indices to which a GPU is directly connected.
    Use either the device index or the specified device identifier UUID.

    Parameters
    ----------
    device_index: int or str
        The index or UUID of the device from which to obtain the CPU affinity.

    Examples
    --------
    >>> from dask_cuda.utils import get_cpu_affinity
    >>> get_cpu_affinity(0)  # DGX-1 has GPUs 0-3 connected to CPUs [0-19, 20-39]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
     40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    >>> get_cpu_affinity(5)  # DGX-1 has GPUs 5-7 connected to CPUs [20-39, 60-79]
    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
     60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]
    >>> get_cpu_affinity(1000)  # DGX-1 has no device on index 1000
    dask_cuda/utils.py:96: UserWarning: Cannot get CPU affinity for device with index
    1000, setting default affinity
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
     20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
     40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
     60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]
    """

def get_n_gpus(): ...
def get_device_total_memory(device_index: int = 0):
    """Return total memory of CUDA device with index or with device identifier UUID.

    Parameters
    ----------
    device_index: int or str
        The index or UUID of the device from which to obtain the CPU affinity.

    Returns
    -------
    The total memory of the CUDA Device in bytes, or ``None`` for devices that do not
    have a dedicated memory resource, as is usually the case for system on a chip (SoC)
    devices.
    """

def has_device_memory_resource(device_index: int = 0):
    """Determine wheter CUDA device has dedicated memory resource.

    Certain devices have no dedicated memory resource, such as system on a chip (SoC)
    devices.

    Parameters
    ----------
    device_index: int or str
        The index or UUID of the device from which to obtain the CPU affinity.

    Returns
    -------
    Whether the device has a dedicated memory resource.
    """

def warn_about_nvlink_if_not_suppressed(
    rocm_ipc_enabled: bool = True, rocm_ipc_opt_name: str = "enable_rocm_ipc"
): ...
def get_ucx_config(
    enable_tcp_over_ucx=None,
    enable_infiniband=None,
    enable_rocm_ipc=None,
    enable_rdmacm=None,
    enable_nvlink=None,
): ...
def get_preload_options(
    protocol=None,
    create_cuda_context=None,
    enable_tcp_over_ucx=None,
    enable_infiniband=None,
    enable_rocm_ipc=None,
    enable_rdmacm=None,
    enable_nvlink=None,
):
    """
    Return a dictionary with the preload and preload_argv options required to
    create CUDA context and enabling UCX communication.

    Parameters
    ----------
    protocol: None or str, default None
        If "ucx", options related to UCX (enable_tcp_over_ucx, enable_infiniband,
        enable_rocm_ipc) are added to preload_argv.
    create_cuda_context: bool, default None
        Ensure the CUDA context gets created at initialization, generally
        needed by Dask workers.
    enable_tcp: bool, default None
        Set environment variables to enable TCP over UCX, even when InfiniBand or
        NVLink support are disabled.
    enable_infiniband: bool, default None
        Set environment variables to enable UCX InfiniBand support. Implies
        enable_tcp=True.
    enable_rdmacm: bool, default None
        Set environment variables to enable UCX RDMA connection manager support.
        Currently requires enable_infiniband=True.
    enable_rocm_ipc: bool, default None
        Set environment variables to enable UCX rocm_ipc support. Implies
        enable_tcp=True.

    Example
    -------
    >>> from dask_cuda.utils import get_preload_options
    >>> get_preload_options()
    {\'preload\': [\'dask_cuda.initialize\'], \'preload_argv\': []}
    >>> get_preload_options(protocol="ucx",
    ...                     create_cuda_context=True,
    ...                     enable_infiniband=True)
    {\'preload\': [\'dask_cuda.initialize\'],
     \'preload_argv\': [\'--create-cuda-context\',
      \'--enable-infiniband\']}
    """

def get_rmm_log_file_name(dask_worker, logging: bool = False, log_directory=None): ...
def wait_workers(
    client,
    min_timeout: int = 10,
    seconds_per_gpu: int = 2,
    n_gpus=None,
    timeout_callback=None,
):
    """
    Wait for workers to be available. When a timeout occurs, a callback
    is executed if specified. Generally used for tests.

    Parameters
    ----------
    client: distributed.Client
        Instance of client, used to query for number of workers connected.
    min_timeout: float
        Minimum number of seconds to wait before timeout. This value may be
        overridden by setting the ``DASK_CUDA_WAIT_WORKERS_MIN_TIMEOUT`` with
        a positive integer.
    seconds_per_gpu: float
        Seconds to wait for each GPU on the system. For example, if its
        value is 2 and there is a total of 8 GPUs (workers) being started,
        a timeout will occur after 16 seconds. Note that this value is only
        used as timeout when larger than min_timeout.
    n_gpus: None or int
        If specified, will wait for a that amount of GPUs (i.e., Dask workers)
        to come online, else waits for a total of ``get_n_gpus`` workers.
    timeout_callback: None or callable
        A callback function to be executed if a timeout occurs, ignored if
        None.

    Returns
    -------
    True if all workers were started, False if a timeout occurs.
    """

def all_to_all(client): ...
def parse_cuda_visible_device(dev):
    """Parses a single CUDA device identifier

    A device identifier must either be an integer, a string containing an
    integer or a string containing the device's UUID, beginning with prefix
    'GPU-' or 'MIG-'.

    >>> parse_cuda_visible_device(2)
    2
    >>> parse_cuda_visible_device('2')
    2
    >>> parse_cuda_visible_device('GPU-9baca7f5-0f2f-01ac-6b05-8da14d6e9005')
    'GPU-9baca7f5-0f2f-01ac-6b05-8da14d6e9005'
    >>> parse_cuda_visible_device('Foo')
    Traceback (most recent call last):
    ...
    ValueError: Devices in CUDA_VISIBLE_DEVICES must be comma-separated integers or
    strings beginning with 'GPU-' or 'MIG-' prefixes.
    """

def cuda_visible_devices(i, visible=None):
    """Cycling values for CUDA_VISIBLE_DEVICES environment variable

    Examples
    --------
    >>> cuda_visible_devices(0, range(4))
    '0,1,2,3'
    >>> cuda_visible_devices(3, range(8))
    '3,4,5,6,7,0,1,2'
    """

def nvml_device_index(i, CUDA_VISIBLE_DEVICES):
    """Get the device index for NVML addressing

    NVML expects the index of the physical device, unlike CUDA runtime which
    expects the address relative to ``CUDA_VISIBLE_DEVICES``. This function
    returns the i-th device index from the ``CUDA_VISIBLE_DEVICES``
    comma-separated string of devices or list.

    Examples
    --------
    >>> nvml_device_index(1, "0,1,2,3")
    1
    >>> nvml_device_index(1, "1,2,3,0")
    2
    >>> nvml_device_index(1, [0,1,2,3])
    1
    >>> nvml_device_index(1, [1,2,3,0])
    2
    >>> nvml_device_index(1, ["GPU-84fd49f2-48ad-50e8-9f2e-3bf0dfd47ccb",
                              "GPU-d6ac2d46-159b-5895-a854-cb745962ef0f",
                              "GPU-158153b7-51d0-5908-a67c-f406bc86be17"])
    "MIG-d6ac2d46-159b-5895-a854-cb745962ef0f"
    >>> nvml_device_index(2, ["MIG-41b3359c-e721-56e5-8009-12e5797ed514",
                              "MIG-65b79fff-6d3c-5490-a288-b31ec705f310",
                              "MIG-c6e2bae8-46d4-5a7e-9a68-c6cf1f680ba0"])
    "MIG-c6e2bae8-46d4-5a7e-9a68-c6cf1f680ba0"
    >>> nvml_device_index(1, 2)
    Traceback (most recent call last):
    ...
    ValueError: CUDA_VISIBLE_DEVICES must be `str` or `list`
    """

def parse_device_bytes(device_bytes, device_index: int = 0, alignment_size: int = 1):
    """Parse bytes relative to a specific CUDA device.

    Parameters
    ----------
    device_bytes: float, int, str or None
        Can be an integer (bytes), float (fraction of total device memory), string
        (like ``"5GB"`` or ``"5000M"``), ``0`` and ``None`` are special cases
        returning ``None``.
    device_index: int or str
        The index or UUID of the device from which to obtain the total memory amount.
        Default: 0.
    alignment_size: int
        Number of bytes of alignment to use, i.e., allocation must be a multiple of
        that size. RMM pool requires 256 bytes alignment.

    Returns
    -------
    The parsed bytes value relative to the CUDA devices, or ``None`` as convenience if
    ``device_bytes`` is ``None`` or any value that would evaluate to ``0``.

    Examples
    --------
    >>> # On a 32GB CUDA device
    >>> parse_device_bytes(None)
    None
    >>> parse_device_bytes(0)
    None
    >>> parse_device_bytes(0.0)
    None
    >>> parse_device_bytes("0 MiB")
    None
    >>> parse_device_bytes(1.0)
    34089730048
    >>> parse_device_bytes(0.8)
    27271784038
    >>> parse_device_bytes(1000000000)
    1000000000
    >>> parse_device_bytes("1GB")
    1000000000
    >>> parse_device_bytes("1GB")
    1000000000
    """

def parse_device_memory_limit(
    device_memory_limit, device_index: int = 0, alignment_size: int = 1
):
    """Parse memory limit to be used by a CUDA device.

    Parameters
    ----------
    device_memory_limit: float, int, str or None
        Can be an integer (bytes), float (fraction of total device memory), string
        (like ``"5GB"`` or ``"5000M"``), ``"auto"``, ``0`` or ``None`` to disable
        spilling to host (i.e. allow full device memory usage). Another special value
        ``"default"`` is also available and returns the recommended Dask-CUDA\'s defaults
        and means 80% of the total device memory (analogous to ``0.8``), and disabled
        spilling (analogous to ``auto``/``0``/``None``) on devices without a dedicated
        memory resource, such as system on a chip (SoC) devices.
    device_index: int or str
        The index or UUID of the device from which to obtain the total memory amount.
        Default: 0.
    alignment_size: int
        Number of bytes of alignment to use, i.e., allocation must be a multiple of
        that size. RMM pool requires 256 bytes alignment.

    Returns
    -------
    The parsed memory limit in bytes, or ``None`` as convenience if
    ``device_memory_limit`` is ``None`` or any value that would evaluate to ``0``.

    Examples
    --------
    >>> # On a 32GB CUDA device
    >>> parse_device_memory_limit(None)
    None
    >>> parse_device_memory_limit(0)
    None
    >>> parse_device_memory_limit(0.0)
    None
    >>> parse_device_memory_limit("0 MiB")
    None
    >>> parse_device_memory_limit(1.0)
    34089730048
    >>> parse_device_memory_limit(0.8)
    27271784038
    >>> parse_device_memory_limit(1000000000)
    1000000000
    >>> parse_device_memory_limit("1GB")
    1000000000
    >>> parse_device_memory_limit("1GB")
    1000000000
    >>> parse_device_memory_limit("auto") == (
    ...    parse_device_memory_limit(1.0)
    ...    if has_device_memory_resource()
    ...    else None
    ... )
    True
    >>> parse_device_memory_limit("default") == (
    ...    parse_device_memory_limit(0.8)
    ...    if has_device_memory_resource()
    ...    else None
    ... )
    True
    """

def get_gpu_uuid(device_index: int = 0):
    """Get GPU UUID from CUDA device index.

    Parameters
    ----------
    device_index: int or str
        The index or UUID of the device from which to obtain the UUID.

    Examples
    --------
    >>> get_gpu_uuid()
    \'GPU-9baca7f5-0f2f-01ac-6b05-8da14d6e9005\'

    >>> get_gpu_uuid(3)
    \'GPU-9fb42d6f-7d6b-368f-f79c-3c3e784c93f6\'

    >>> get_gpu_uuid("GPU-9fb42d6f-7d6b-368f-f79c-3c3e784c93f6")
    \'GPU-9fb42d6f-7d6b-368f-f79c-3c3e784c93f6\'
    """

def get_worker_config(dask_worker): ...
async def get_scheduler_configuration(client): ...
@singledispatch
def pretty_print(obj, toplevel): ...
def pretty_print_str(obj, toplevel): ...
def pretty_print_dict(obj, toplevel): ...
def print_cluster_config(client) -> None:
    """print current Dask cluster configuration"""

def get_cluster_configuration(client): ...
def get_rmm_device_memory_usage() -> int | None:
    """Get current bytes allocated on current device through RMM

    Check the current RMM resource stack for resources such as
    ``StatisticsResourceAdaptor`` and ``TrackingResourceAdaptor``
    that can report the current allocated bytes. Returns None,
    if no such resources exist.

    Return
    ------
    nbytes: int or None
        Number of bytes allocated on device through RMM or None
    """

class CommaSeparatedChoice(click.Choice):
    def convert(self, value, param, ctx): ...
