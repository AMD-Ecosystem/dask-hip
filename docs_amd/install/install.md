<!-- SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc. -->
<!-- SPDX-License-Identifier: MIT -->

<head>
  <meta charset="UTF-8">
  <meta name="description" content="dask-hip installation guide">
  <meta name="keywords" content="Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, install">
</head>

# Installing dask-hip

You can install dask-hip via AMD PyPI as described below. This is recommended for users of the package. For developers interested in modifying or contributing to the open-source dask-hip component, see the [Build instructions](./build.md).

## Requirements

dask-hip requires ROCm 7.2 running on a [ROCm-supported operating system](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-operating-systems). Using Ubuntu 22.04 or later is recommended. For more information, see [ROCm-DS system requirements](https://rocm.docs.amd.com/projects/rocm-ds/en/latest/install/requirements.html).

The steps in this topic require a Conda installation. A minimal free version of Conda is [Miniforge](https://conda-forge.org/download/).

## Install dask-hip via AMD PyPI

Packaged versions of dask-hip and its dependencies are distributed via [AMD PyPI](https://pypi.amd.com/simple). This section describes how to install dask-hip via this package index.

Create and activate a Conda environment with Python 3.12 as shown below:

```bash
conda create --name dask-hip python=3.12
conda activate dask-hip
```

dask-hip can then be installed into this environment using pip and the AMD PyPI URL:

```bash
pip install amd-dask-hip --extra-index-url=https://pypi.amd.com/simple
```

### hipUCXX support

To install the `distributed-hipucxx` package for high-performance UCX communication (ROCm-IPC, InfiniBand):

```bash
pip install distributed-hipucxx --extra-index-url=https://pypi.amd.com/simple
```

## Other ROCm-DS libraries

dask-hip is part of the [ROCm Data Science (ROCm-DS)](https://rocm.docs.amd.com/projects/rocm-ds/en/latest/) suite and works well in conjunction with other ROCm-DS libraries:

- [hipDF](https://github.com/AMD-AIOSS/hipDF) -- GPU-accelerated DataFrames
- [hipRaft](https://github.com/AMD-AIOSS/hipRaft) -- GPU-accelerated machine learning primitives
- [hipUCXX](https://github.com/AMD-AIOSS/hipUCXX) -- High-performance UCX communication
