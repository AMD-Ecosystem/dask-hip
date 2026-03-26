.. meta::
  :description: dask-hip documentation and API reference
  :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, RAPIDS, data science

.. _dask-hip:

********************************************************************
dask-hip documentation
********************************************************************

dask-hip is an extension of `Dask.distributed <https://distributed.dask.org/en/latest/>`_ for
multi-GPU computing on AMD hardware. It is part of the AMD ROCm Data Science toolkit (ROCm-DS),
an open-source software collection for high-performance data science applications. Forked from the
`NVIDIA RAPIDS dask-cuda <https://github.com/rapidsai/dask-cuda>`_ project, dask-hip brings the
same distributed GPU computing capabilities to the :doc:`ROCm <rocm:index>`/:doc:`HIP <hip:index>`
stack while preserving API compatibility. For more information,
see :doc:`What is dask-hip? <what-is-dask-hip>`

The dask-hip code is open and hosted at
`https://github.com/AMD-AIOSS/dask-hip <https://github.com/AMD-AIOSS/dask-hip>`_.

.. grid:: 2
  :gutter: 3

  .. grid-item-card:: Installation

    * :doc:`System requirements <install/system-requirements>`
    * :doc:`Installing dask-hip <install/install>`
    * :doc:`Building from source <install/build>`

  .. grid-item-card:: How to

    * :doc:`Using dask-hip <how-to/using-dask-hip>`

  .. grid-item-card:: API reference

    * :doc:`Python API reference <reference/api>`

To contribute to the documentation refer to
`Contributing to ROCm-DS  <https://rocm.docs.amd.com/projects/rocm-ds/en/latest/contribute/contributing.html>`_.

You can find licensing information on the
`Licensing <https://rocm.docs.amd.com/projects/rocm-ds/en/latest/about/license.html>`_ page.
