.. meta::
   :description: dask-hip installation guide
   :keywords: Dask, GPU, distributed computing, HIP, ROCm, AMD Data Science, install

.. _install:

*******************
Installing dask-hip
*******************

You can install dask-hip via AMD PyPI as described below. This is recommended for users of the
package. For developers interested in modifying or contributing to the open-source dask-hip
component, see the :doc:`Build instructions <build>`.

See :ref:`system-requirements` for information regarding supported operating systems, ROCm versions,
and AMD GPUs before installing dask-hip.

ROCm component prerequisites
============================

dask-hip requires the ``amdsmi`` Python package, which is distributed with ROCm (not via AMD
PyPI). Install it from the ROCm installation before installing dask-hip. See `AMD SMI documentation <https://rocm.docs.amd.com/projects/amdsmi/en/docs-7.2.3/index.html>`__ for more information.

.. code-block:: bash

   cd /opt/rocm/share/amd_smi
   pip install .

Install dask-hip via AMD PyPI
==============================

Packaged versions of dask-hip and its dependencies are distributed via
`AMD PyPI <https://pypi.amd.com/rocm-7.2.3/simple/>`_. This section describes how to install dask-hip via this
package index.

Create and activate a Conda environment with a compatible Python version, such as 3.11 or 3.12 as shown below. For more information on compatible Python versions, see :ref:`system-requirements`.

.. code-block:: bash

   conda create --name dask-hip python=3.12 # Specify your Python version
   conda activate dask-hip

Alternatively, create a Python virtual environment:

.. code-block:: bash

   python3 -m venv dask-hip-env
   source dask-hip-env/bin/activate

dask-hip can then be installed into either environment using pip and the AMD PyPI URL:

.. code-block:: bash

   pip install amd-dask-hip --extra-index-url=https://pypi.amd.com/rocm-7.2.3/simple/

hip-ucxx support
---------------

To install the ``amd-distributed-hipucxx`` package for high-performance UCX communication
(ROCm-IPC, InfiniBand):

.. code-block:: bash

   pip install amd-distributed-hipucxx --extra-index-url=https://pypi.amd.com/rocm-7.2.3/simple/

pynvml compatibility
--------------------

dask-hip bundles a ``pynvml2amdsmi`` compatibility shim that maps ``pynvml`` API calls to their
AMD SMI equivalents. This allows upstream packages such as ``dask.distributed`` to query GPU
information transparently on AMD hardware without modification.
