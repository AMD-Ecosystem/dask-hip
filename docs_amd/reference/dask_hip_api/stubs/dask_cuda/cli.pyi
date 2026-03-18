import click
from _typeshed import Incomplete

from .cuda_worker import CUDAWorker as CUDAWorker
from .utils import (
    CommaSeparatedChoice as CommaSeparatedChoice,
    print_cluster_config as print_cluster_config,
    warn_about_nvlink_if_not_suppressed as warn_about_nvlink_if_not_suppressed,
)

logger: Incomplete
pem_file_option_type: Incomplete
scheduler: Incomplete
preload_argv: Incomplete
scheduler_file: Incomplete
tls_ca_file: Incomplete
tls_cert: Incomplete
tls_key: Incomplete

@click.group
def cuda() -> None:
    """Subcommands to launch or query distributed workers with GPUs."""

@scheduler
@preload_argv
@scheduler_file
@tls_ca_file
@tls_cert
@tls_key
def worker(
    scheduler,
    host,
    nthreads,
    name,
    memory_limit,
    device_memory_limit,
    enable_cudf_spill,
    cudf_spill_stats,
    rmm_pool_size,
    rmm_maximum_pool_size,
    rmm_managed_memory,
    rmm_async,
    rmm_allocator_external_lib_list,
    rmm_release_threshold,
    rmm_log_directory,
    rmm_track_allocations,
    pid_file,
    resources,
    dashboard,
    dashboard_address,
    local_directory,
    shared_filesystem,
    scheduler_file,
    interface,
    preload,
    dashboard_prefix,
    tls_ca_file,
    tls_cert,
    tls_key,
    enable_tcp_over_ucx,
    enable_infiniband,
    enable_rocm_ipc,
    enable_rdmacm,
    enable_jit_unspill,
    worker_class,
    pre_import,
    multiprocessing_method,
    enable_nvlink,
    **kwargs
) -> None:
    """Launch a distributed worker with GPUs attached to an existing scheduler.

    A scheduler can be specified either through a URI passed through the ``SCHEDULER``
    argument or a scheduler file passed through the ``--scheduler-file`` option.

    See
    https://docs.rapids.ai/api/dask-cuda/stable/quickstart.html#dask-cuda-worker
    for info.
    """

@scheduler
@preload_argv
@scheduler_file
@tls_ca_file
@tls_cert
@tls_key
def config(scheduler, scheduler_file, tls_ca_file, tls_cert, tls_key, **kwargs) -> None:
    """Query an existing GPU cluster's configuration.

    A cluster can be specified either through a URI passed through the ``SCHEDULER``
    argument or a scheduler file passed through the ``--scheduler-file`` option.
    """
