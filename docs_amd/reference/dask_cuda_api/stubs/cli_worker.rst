Launch a distributed worker with GPUs attached to an existing scheduler.

A scheduler can be specified either through a URI passed through the ``SCHEDULER``
argument or a scheduler file passed through the ``--scheduler-file`` option.

See
https://docs.rapids.ai/api/dask-cuda/stable/quickstart.html#dask-cuda-worker
for info.

.. program:: dask cuda worker
.. rubric:: Usage

.. code-block:: shell

    dask cuda worker [OPTIONS] [SCHEDULER] [PRELOAD_ARGV]...

.. rubric:: Options

.. option:: --host <host>

    IP address of serving host; should be visible to the scheduler and other
    workers. Can be a string (like ``"127.0.0.1"``) or ``None`` to fall back on the
    address of the interface specified by ``--interface`` or the default interface.

.. option:: --nthreads <nthreads>

    Number of threads to be used for each Dask worker process.

    :default: ``1``

.. option:: --name <name>

    A unique name for the worker. Can be a string (like ``"worker-1"``) or
    ``None`` for a nameless worker.

.. option:: --memory-limit <memory_limit>

    Size of the host LRU cache, which is used to determine when the worker
    starts spilling to disk (not available if JIT-Unspill is enabled). Can be an
    integer (bytes), float (fraction of total system memory), string (like ``"5GB"``
    or ``"5000M"``), or ``"auto"`` or ``0`` for no memory management.

    :default: ``'auto'``

.. option:: --device-memory-limit <device_memory_limit>

    Size of the CUDA device LRU cache, which is used to determine when the
    worker starts spilling to host memory. Can be an integer (bytes), float (fraction of
    total device memory), string (like ``"5GB"`` or ``"5000M"``), ``"auto"`` or ``0``
    to disable spilling to host (i.e. allow full device memory usage). Another special
    value ``"default"`` (which happens to be the default) is also available and uses the
    recommended Dask-CUDA's defaults and means 80% of the total device memory (analogous
    to ``0.8``), and disabled spilling (analogous to ``auto``/``0``) on devices without
    a dedicated memory resource, such as system on a chip (SoC) devices.

    :default: ``'default'``

.. option:: --enable-cudf-spill, --disable-cudf-spill

    Enable automatic cuDF spilling. WARNING: This should NOT be used with
    JIT-Unspill.

    :default: ``False``

.. option:: --cudf-spill-stats <cudf_spill_stats>

    Set the cuDF spilling statistics level. This option has no effect if
    ``--enable-cudf-spill`` is not specified.

.. option:: --rmm-pool-size <rmm_pool_size>

    RMM pool size to initialize each worker with. Can be an integer (bytes),
    float (fraction of total device memory), string (like ``"5GB"`` or ``"5000M"``), or
    ``None`` to disable RMM pools.

    .. note::
        This size is a per-worker configuration, and not cluster-wide.

.. option:: --rmm-maximum-pool-size <rmm_maximum_pool_size>

    When ``--rmm-pool-size`` is specified, this argument indicates the maximum
    pool size.  Can be an integer (bytes), float (fraction of total device memory),
    string (like ``"5GB"`` or ``"5000M"``) or ``None``. By default, the total available
    memory on the GPU is used. ``rmm_pool_size`` must be specified to use RMM pool and
    to set the maximum pool size.

    .. note::
        When paired with ``--enable-rmm-async`` the maximum size cannot be guaranteed
        due to fragmentation.

    .. note::
        This size is a per-worker configuration, and not cluster-wide.

.. option:: --rmm-managed-memory, --no-rmm-managed-memory

    Initialize each worker with RMM and set it to use managed memory. If
    disabled, RMM may still be used by specifying ``--rmm-pool-size``.

    .. warning::
        Managed memory is currently incompatible with NVLink. Trying to enable both will
        result in failure.

    :default: ``False``

.. option:: --rmm-async, --no-rmm-async

    Initialize each worker with RMM and set it to use RMM's asynchronous
    allocator. See ``rmm.mr.CudaAsyncMemoryResource`` for more info.

    .. warning::
        The asynchronous allocator is incompatible with RMM pools and managed memory,
        trying to enable both will result in failure.

    :default: ``False``

.. option:: --set-rmm-allocator-for-libs <rmm_allocator_external_lib_list>

    Set RMM as the allocator for external libraries. Provide a comma-separated
    list of libraries to set, e.g., "torch,cupy".

    :options: cupy | torch

.. option:: --rmm-release-threshold <rmm_release_threshold>

    When ``rmm.async`` is ``True`` and the pool size grows beyond this
    value, unused memory held by the pool will be released at the next
    synchronization point. Can be an integer (bytes), float (fraction of total
    device memory), string (like ``"5GB"`` or ``"5000M"``) or ``None``. By
    default, this feature is disabled.

    .. note::
        This size is a per-worker configuration, and not cluster-wide.

.. option:: --rmm-log-directory <rmm_log_directory>

    Directory to write per-worker RMM log files to. The client and scheduler are
    not logged here. Can be a string (like ``"/path/to/logs/"``) or ``None`` to disable
    logging.

    .. note::
        Logging will only be enabled if ``--rmm-pool-size`` or ``--rmm-managed-memory``
        are specified.

.. option:: --rmm-track-allocations, --no-rmm-track-allocations

    Track memory allocations made by RMM. If ``True``, wraps the memory
    resource of each worker with a ``rmm.mr.TrackingResourceAdaptor`` that
    allows querying the amount of memory allocated by RMM.

    :default: ``False``

.. option:: --pid-file <pid_file>

    File to write the process PID.

.. option:: --resources <resources>

    Resources for task constraints like ``"GPU=2 MEM=10e9"``.

.. option:: --dashboard, --no-dashboard

    Launch the dashboard.

    :default: ``True``

.. option:: --dashboard-address <dashboard_address>

    Relative address to serve the dashboard (if enabled).

    :default: ``':0'``

.. option:: --local-directory <local_directory>

    Path on local machine to store temporary files. Can be a string (like
    ``"path/to/files"``) or ``None`` to fall back on the value of
    ``dask.temporary-directory`` in the local Dask configuration, using the current
    working directory if this is not set.

.. option:: --shared-filesystem, --no-shared-filesystem

    If ``--shared-filesystem`` is specified, inform JIT-Unspill that
    ``local_directory`` is a shared filesystem available for all workers, whereas
    ``--no-shared-filesystem`` informs it may not assume it's a shared filesystem.
    If neither is specified, JIT-Unspill will decide based on the Dask config value
    specified by ``"jit-unspill-shared-fs"``.
    Notice, a shared filesystem must support the ``os.link()`` operation.

.. option:: --scheduler-file <scheduler_file>

    Filename to JSON encoded scheduler information. To be used in conjunction
    with the equivalent ``dask scheduler`` option.

.. option:: --protocol <protocol>

    Protocol like tcp, tls, or ucx

.. option:: --interface <interface>

    External interface used to connect to the scheduler. Usually an ethernet
    interface is used for connection, and not an InfiniBand interface (if one is
    available). Can be a string (like ``"eth0"`` for NVLink or ``"ib0"`` for
    InfiniBand) or ``None`` to fall back on the default interface.

.. option:: --preload <preload>

    Module that should be loaded by each worker process like ``"foo.bar"`` or
    ``"/path/to/foo.py"``.

.. option:: --death-timeout <death_timeout>

    Seconds to wait for a scheduler before closing

.. option:: --dashboard-prefix <dashboard_prefix>

    Prefix for the dashboard. Can be a string (like ...) or ``None`` for no
    prefix.

.. option:: --tls-ca-file <tls_ca_file>

    CA certificate(s) file for TLS (in PEM format). Can be a string (like
    ``"path/to/certs"``), or ``None`` for no certificate(s).

.. option:: --tls-cert <tls_cert>

    Certificate file for TLS (in PEM format). Can be a string (like
    ``"path/to/certs"``), or ``None`` for no certificate(s).

.. option:: --tls-key <tls_key>

    Private key file for TLS (in PEM format). Can be a string (like
    ``"path/to/certs"``), or ``None`` for no private key.

.. option:: --enable-tcp-over-ucx, --disable-tcp-over-ucx

    Set environment variables to enable TCP over UCX, even if InfiniBand and
    NVLink are not supported or disabled.

.. option:: --enable-infiniband, --disable-infiniband

    Set environment variables to enable UCX over InfiniBand, implies
    ``--enable-tcp-over-ucx`` when enabled.

.. option:: --enable-rocm-ipc, --disable-rocm-ipc

    Set environment variables to enable rocm_ipc TL for UCX, implies
    ``--enable-tcp-over-ucx`` when enabled.

.. option:: --enable-nvlink, --disable-nvlink

    Same effect as ``--enable-rocm-ipc/--disable-rocm-ipc``, as NVLink in not
    valid/supported for AMD. Only supported for easy portability. A warning will be
    shown unless suppressed using the 'DASK_HIP_SUPPRESS_NVLINK_WARNING' environment
    variable. Please use ``--enable-rocm-ipc/--disable-rocm-ipc`` instead.

.. option:: --enable-rdmacm, --disable-rdmacm

    Set environment variables to enable UCX RDMA connection manager support,
    requires ``--enable-infiniband``.

.. option:: --enable-jit-unspill, --disable-jit-unspill

    Enable just-in-time unspilling. Can be a boolean or ``None`` to fall back on
    the value of ``dask.jit-unspill`` in the local Dask configuration, disabling
    unspilling if this is not set.

    .. note::
        This is experimental and doesn't support memory spilling to disk. See
        ``proxy_object.ProxyObject`` and ``proxify_host_file.ProxifyHostFile`` for more
        info.

.. option:: --worker-class <worker_class>

    Use a different class than Distributed's default (``distributed.Worker``)
    to spawn ``distributed.Nanny``.

.. option:: --pre-import <pre_import>

    Pre-import libraries as a Worker plugin to prevent long import times
    bleeding through later Dask operations. Should be a list of comma-separated names,
    such as "cudf,rmm".

.. option:: --multiprocessing-method <multiprocessing_method>

    Method used to start new processes with multiprocessing

    :options: spawn | fork | forkserver

.. rubric:: Arguments

.. option:: SCHEDULER

    Optional argument

.. option:: PRELOAD_ARGV

    Optional argument(s)
