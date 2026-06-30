.. meta::
   :description: dask-hip system requirements
   :keywords: Dask, GPU, HIP, ROCm, ROCm-DS, AMD, requirements, compatibility

.. _system-requirements:

*******************
System requirements
*******************

This topic lists the system requirements for using dask-hip.

* ROCm version: `7.2.3 <https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.3/>`__
* Operating Systems: Ubuntu 24.04 and 22.04
* Supported AMD Instinct GPUs:

  - MI355X (GPU target gfx950)
  - MI325X / MI300X (GPU target gfx942)
  - MI250 / MI210 (GPU target gfx90a)

* Python versions: 3.10, 3.11, 3.12, 3.13

Conda or virtual environment
-----------------------------

A Conda installation or Python virtual environment is recommended for managing dependencies, such as
`Miniforge <https://conda-forge.org/download/>`_ as a minimal Conda distribution.
