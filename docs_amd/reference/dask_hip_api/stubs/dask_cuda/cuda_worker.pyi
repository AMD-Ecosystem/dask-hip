from _typeshed import Incomplete

from distributed.core import Server

from .initialize import initialize as initialize
from .utils import (
    cuda_visible_devices as cuda_visible_devices,
    get_n_gpus as get_n_gpus,
    get_ucx_config as get_ucx_config,
    nvml_device_index as nvml_device_index,
    warn_about_nvlink_if_not_suppressed as warn_about_nvlink_if_not_suppressed,
)
from .worker_common import (
    worker_data_function as worker_data_function,
    worker_plugins as worker_plugins,
)

class CUDAWorker(Server):
    nannies: Incomplete
    def __init__(
        self,
        scheduler=None,
        host=None,
        nthreads: int = 1,
        name=None,
        memory_limit: str = "auto",
        device_memory_limit: str = "default",
        enable_cudf_spill: bool = False,
        cudf_spill_stats: int = 0,
        rmm_pool_size=None,
        rmm_maximum_pool_size=None,
        rmm_managed_memory: bool = False,
        rmm_async: bool = False,
        rmm_allocator_external_lib_list=None,
        rmm_release_threshold=None,
        rmm_log_directory=None,
        rmm_track_allocations: bool = False,
        pid_file=None,
        resources=None,
        dashboard: bool = True,
        dashboard_address: str = ":0",
        local_directory=None,
        shared_filesystem=None,
        scheduler_file=None,
        interface=None,
        preload=[],
        dashboard_prefix=None,
        security=None,
        enable_tcp_over_ucx=None,
        enable_infiniband=None,
        enable_rocm_ipc=None,
        enable_rdmacm=None,
        jit_unspill=None,
        worker_class=None,
        pre_import=None,
        enable_nvlink=None,
        **kwargs
    ) -> None: ...
    def __await__(self): ...
    async def finished(self) -> None: ...
    async def close(self, timeout: int = 5) -> None: ...
