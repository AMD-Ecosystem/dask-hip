from .device_host_file import DeviceHostFile as DeviceHostFile
from .plugins import (
    CPUAffinity as CPUAffinity,
    CUDFSetup as CUDFSetup,
    PreImport as PreImport,
    RMMSetup as RMMSetup,
)
from .proxify_host_file import ProxifyHostFile as ProxifyHostFile
from .utils import (
    get_cpu_affinity as get_cpu_affinity,
    has_device_memory_resource as has_device_memory_resource,
    parse_device_memory_limit as parse_device_memory_limit,
)

def worker_data_function(
    device_memory_limit=None,
    memory_limit=None,
    jit_unspill: bool = False,
    enable_cudf_spill: bool = False,
    shared_filesystem=None,
):
    """
    Create a data function for CUDA workers based on memory configuration.

    This function creates and returns a callable that generates data configuration
    for CUDA workers. The returned callable takes a device index parameter and
    returns the appropriate data configuration for that device.

    Parameters
    ----------
    device_memory_limit : str or int, optional
        Limit of device memory, defaults to None
    memory_limit : str or int, optional
        Limit of host memory, defaults to None
    jit_unspill : bool, optional
        Whether to enable JIT unspill functionality, defaults to False
    enable_cudf_spill : bool, optional
        Whether to enable cuDF spilling, defaults to False
    shared_filesystem : str or bool, optional
        Whether to use shared filesystem for spilling, defaults to None

    Returns
    -------
    callable
        A function that takes device index `device_index` and returns appropriate
        data configuration based on the availability of an dedicated device memory
        resource and arguments passed to the worker.
    """

def worker_plugins(
    *,
    device_index,
    rmm_initial_pool_size,
    rmm_maximum_pool_size,
    rmm_managed_memory,
    rmm_async_alloc,
    rmm_release_threshold,
    rmm_log_directory,
    rmm_track_allocations,
    rmm_allocator_external_lib_list,
    pre_import,
    enable_cudf_spill,
    cudf_spill_stats
):
    """Create a set of plugins for CUDA workers with specified configurations.

    This function creates and returns a set of plugins that configure various aspects
    of CUDA worker behavior, including CPU affinity, RMM memory management, pre-import
    modules and cuDF spilling functionality.

    Parameters
    ----------
    device_index : int
        The CUDA device index to configure
    rmm_initial_pool_size : int or str
        Initial size of the RMM memory pool
    rmm_maximum_pool_size : int or str
        Maximum size of the RMM memory pool
    rmm_managed_memory : bool
        Whether to use CUDA managed memory
    rmm_async_alloc : bool
        Whether to use asynchronous allocation
    rmm_release_threshold : int
        Memory threshold for releasing memory back to the system
    rmm_log_directory : str
        Directory for RMM logging
    rmm_track_allocations : bool
        Whether to track memory allocations
    rmm_allocator_external_lib_list : list
        List of external libraries to use with RMM allocator
    pre_import : list
        List of modules to pre-import
    enable_cudf_spill : bool
        Whether to enable cuDF spilling
    cudf_spill_stats : bool
        Whether to track cuDF spilling statistics

    Returns
    -------
    set
        A set of configured plugins including:
        - CPUAffinity: Configures CPU affinity for the worker
        - RMMSetup: Configures RMM memory management
        - PreImport: Handles module pre-importing
        - CUDFSetup: Configures cuDF functionality and spilling
    """
