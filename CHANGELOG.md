# Changelog

dask-hip is AMD's port of NVIDIA's dask-cuda, enabling multi-GPU Dask clusters
on AMD GPUs via the HIP/ROCm platform. It is part of the AMD Data Science
ecosystem.

Upstream dask-cuda changes are tracked separately in
[`._upstream/CHANGELOG.md`](._upstream/CHANGELOG.md).

## [Release Version 2.0.0 / AMD Data Science 26.09]

### Features
- Updated to upstream dask-cuda 26.06, bringing in its new features and bug fixes.
- Removed the bundled `pynvml` shim, replaced by the `pynvml` provided by `rocm-bindings-hip`.

### Platform Support
- Raised the minimum Python version to 3.11 (dropped 3.10); now supports Python 3.11, 3.12, and 3.13.
- Updated to ROCm 10.0.0.

## [Initial Release Version 1.0.0 / AMD Data Science 26.03]

### Platform Support
- Initial HIP/ROCm port of dask-cuda, targeting upstream dask-cuda 25.10.
- ROCm 7.2.3.
- Ubuntu 22.04 and 24.04.
- AMD Instinct GPUs: MI355X (gfx950), MI325X / MI300X (gfx942), MI250 / MI210 (gfx90a).
- Python 3.10, 3.11, 3.12, and 3.13.

### Features
- Published as `amd-dask-hip`; the `dask_cuda` module name is preserved for drop-in compatibility.
- One-worker-per-GPU scheduling with automatic `HIP_VISIBLE_DEVICES` management and CPU affinity.
- UCX-based high-performance communication (ROCm-IPC, InfiniBand, TCP) via AMD UCXX (`amd-hipucxx`).
- `pynvml` provided by an internal shim shipped with dask-hip.
