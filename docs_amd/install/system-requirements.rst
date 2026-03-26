.. meta::
   :description: dask-hip system requirements
   :keywords: Dask, GPU, HIP, ROCm, ROCm-DS, AMD, requirements, compatibility

.. _system-requirements:

*******************
System requirements
*******************

This topic lists the system requirements for using dask-hip.

* Operating Systems: Ubuntu 24.04 and 22.04
* ROCm version: `7.2.0 <https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.0/>`__ and `7.2.1 <https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.2.1/>`__
* Supported AMD Instinct GPUs:

  - MI350X/MI355X (GPU target gfx950)
  - MI300A/MI300X (GPU target gfx942)
  - MI250X/MI250/MI210 (GPU target gfx90a)

* Python versions: 3.10, 3.11, 3.12

Conda or virtual environment
-----------------------------

A Conda installation or Python virtual environment is recommended for managing dependencies, such as
`Miniforge <https://conda-forge.org/download/>`_ as a minimal Conda distribution.
