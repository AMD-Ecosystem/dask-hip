from .initialize import initialize as initialize
from .local_cuda_cluster import cuda_visible_devices as cuda_visible_devices
from .plugins import CPUAffinity as CPUAffinity
from .utils import (
    get_cpu_affinity as get_cpu_affinity,
    get_gpu_count as get_gpu_count,
    warn_about_nvlink_if_not_suppressed as warn_about_nvlink_if_not_suppressed,
)

def worker_spec(
    interface=None,
    protocol=None,
    dashboard_address: str = ":8787",
    threads_per_worker: int = 1,
    silence_logs: bool = True,
    CUDA_VISIBLE_DEVICES=None,
    enable_tcp_over_ucx: bool = False,
    enable_infiniband: bool = False,
    enable_rocm_ipc: bool = False,
    enable_nvlink=None,
    **kwargs
):
    """Create a Spec for a CUDA worker.

    The Spec created by this function can be used as a recipe for CUDA workers
    that can be passed to a SpecCluster.

    Parameters
    ----------
    interface: str
        The external interface used to connect to the scheduler.
    protocol: str
        The protocol to used for data transfer, e.g., "tcp" or "ucx".
    dashboard_address: str
        The address for the scheduler dashboard.  Defaults to ":8787".
    threads_per_worker: int
        Number of threads to be used for each CUDA worker process.
    silence_logs: bool
        Disable logging for all worker processes
    CUDA_VISIBLE_DEVICES: str
        String like ``"0,1,2,3"`` or ``[0, 1, 2, 3]`` to restrict activity to
        different GPUs
    enable_tcp_over_ucx: bool
        Set environment variables to enable TCP over UCX, even if InfiniBand
        and NVLink are not supported or disabled.
    enable_infiniband: bool
        Set environment variables to enable UCX InfiniBand support. Implies
        enable_tcp_over_ucx=True.
    enable_rocm_ipc: bool
        Set environment variables to enable UCX ROCm-IPC support. Implies
        enable_tcp_over_ucx=True.

    Examples
    --------
    >>> from dask_cuda.worker_spec import worker_spec
    >>> worker_spec(interface="enp1s0f0", CUDA_VISIBLE_DEVICES=[0, 2])
    {0: {\'cls\': distributed.nanny.Nanny,
      \'options\': {\'env\': {\'CUDA_VISIBLE_DEVICES\': \'0,2\'},
       \'interface\': \'enp1s0f0\',
       \'protocol\': None,
       \'nthreads\': 1,
       \'data\': dict,
       \'dashboard_address\': \':8787\',
       \'plugins\': [<dask_cuda.utils.CPUAffinity at 0x7fbb8748a860>],
       \'silence_logs\': True,
       \'memory_limit\': 135263611392.0,
       \'preload\': [\'dask_cuda.initialize\'],
       \'preload_argv\': [\'--create-cuda-context\']}},
     2: {\'cls\': distributed.nanny.Nanny,
      \'options\': {\'env\': {\'CUDA_VISIBLE_DEVICES\': \'2,0\'},
       \'interface\': \'enp1s0f0\',
       \'protocol\': None,
       \'nthreads\': 1,
       \'data\': dict,
       \'dashboard_address\': \':8787\',
       \'plugins\': [<dask_cuda.utils.CPUAffinity at 0x7fbb8748a0f0>],
       \'silence_logs\': True,
       \'memory_limit\': 135263611392.0,
       \'preload\': [\'dask_cuda.initialize\'],
       \'preload_argv\': [\'--create-cuda-context\']}}}

    """
