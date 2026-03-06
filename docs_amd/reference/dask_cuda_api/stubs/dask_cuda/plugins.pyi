from _typeshed import Incomplete

from distributed import WorkerPlugin

from .utils import (
    get_rmm_log_file_name as get_rmm_log_file_name,
    parse_device_bytes as parse_device_bytes,
)

class CPUAffinity(WorkerPlugin):
    cores: Incomplete
    def __init__(self, cores) -> None: ...
    def setup(self, worker=None) -> None: ...

class CUDFSetup(WorkerPlugin):
    spill: Incomplete
    spill_stats: Incomplete
    def __init__(self, spill, spill_stats) -> None: ...
    def setup(self, worker=None) -> None: ...

class RMMSetup(WorkerPlugin):
    initial_pool_size: Incomplete
    maximum_pool_size: Incomplete
    managed_memory: Incomplete
    async_alloc: Incomplete
    release_threshold: Incomplete
    logging: Incomplete
    log_directory: Incomplete
    rmm_track_allocations: Incomplete
    external_lib_list: Incomplete
    def __init__(
        self,
        initial_pool_size,
        maximum_pool_size,
        managed_memory,
        async_alloc,
        release_threshold,
        log_directory,
        track_allocations,
        external_lib_list,
    ) -> None: ...
    def setup(self, worker=None) -> None: ...

def enable_rmm_memory_for_library(lib_name: str) -> None:
    """Enable RMM memory pool support for a specified third-party library.

    This function allows the given library to utilize RMM\'s memory pool if it supports
    integration with RMM. The library name is passed as a string argument, and if the
    library is compatible, its memory allocator will be configured to use RMM.

    Parameters
    ----------
    lib_name : str
        The name of the third-party library to enable RMM memory pool support for.
        Supported libraries are "cupy" and "torch".

    Raises
    ------
    ValueError
        If the library name is not supported or does not have RMM integration.
    ImportError
        If the required library is not installed.
    """

class PreImport(WorkerPlugin):
    libraries: Incomplete
    def __init__(self, libraries) -> None: ...
    def setup(self, worker=None) -> None: ...
