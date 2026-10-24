# dask-hip

dask-hip is an extension of [Dask.distributed](https://distributed.dask.org/)
that simplifies deploying Dask clusters on multi-GPU systems with AMD GPUs. It
is derived from [dask-cuda](https://github.com/rapidsai/dask-cuda) by NVIDIA
Corporation and is part of the [AMD Data Science](https://github.com/AMD-Ecosystem) ecosystem.

Key capabilities include one-worker-per-GPU scheduling with automatic
`HIP_VISIBLE_DEVICES` management, CPU affinity, UCX-based high-performance
communication (ROCm-IPC, InfiniBand, TCP), GPU memory spilling, and hipMM (RMM)
pool integration.

For full documentation, see the
[dask-hip documentation](https://rocm.docs.amd.com/projects/dask-hip/en/latest/).

## Directory layout

```
dask-hip/
├── dask_cuda/            Python package (preserves upstream module name)
│   ├── cli.py              CLI entry point (dask cuda worker, dask cuda config)
│   ├── local_cuda_cluster.py   LocalCUDACluster
│   ├── cuda_worker.py      CUDAWorker
│   ├── initialize.py       Client-side UCX initialization
│   ├── explicit_comms/     Explicit communication API
│   ├── plugins.py          Worker plugins (CPU affinity, RMM, hipDF)
│   └── tests/              Test suite
├── examples/             Usage examples (UCX integration)
├── docs_amd/             Sphinx documentation source
├── scripts/              Utility scripts
├── pyproject.toml        Package metadata and dependencies
└── LICENSE / NOTICE.txt  License files
```

## Environment setup

Create and activate a Python environment before installing or building
dask-hip. Either Conda or a Python virtual environment can be used.

**Conda:**

```bash
conda create --name dask-hip python=3.12
conda activate dask-hip
```

**Python virtual environment:**

```bash
python3 -m venv dask-hip-env
source dask-hip-env/bin/activate
```

## Prerequisites

### AMD SMI

dask-hip queries GPU information through the `pynvml` compatibility shim
provided by `hip-python-interop` (a dependency), which is backed by
`rocm.bindings.amdsmi`. No separate `amdsmi` Python package is required; the
AMD SMI runtime library shipped with ROCm must be installed.

### UCX (optional, for high-performance communication)

UCX-based communication via [hip-ucxx](https://github.com/AMD-AIOSS/hip-ucxx)
enables ROCm-IPC and InfiniBand transports. The hip-ucxx packages depend on
`amd-libucx`, a source-only package that compiles a ROCm-enabled UCX on your
machine during `pip install`, so no separate UCX installation is normally
required (its build prerequisites must be present). See the
[hip-ucxx build guide](https://rocm.docs.amd.com/projects/hip-ucxx/en/latest/install/build.html)
if you prefer to supply UCX yourself.

## Installing

For installing pre-built packages via AMD PyPI, see the
[installation guide](https://rocm.docs.amd.com/projects/dask-hip/en/latest/install/install.html).

For building from source, see the
[build guide](https://rocm.docs.amd.com/projects/dask-hip/en/latest/install/build.html).

## License

dask-hip is licensed under a combination of the Apache License 2.0 (for code
derived from NVIDIA dask-cuda) and the MIT License (for AMD additions). See
[LICENSE](LICENSE) and [NOTICE.txt](NOTICE.txt) for the full license texts.
