.. meta::
   :description: Building dask-hip from source
   :keywords: Dask, GPU, distributed computing, HIP, ROCm, ROCm-DS, AMD, build, source

.. _build:

*********************
Building from source
*********************

The following information is related to building dask-hip from source for developers interested
in modifying and contributing to the projects. Users just interested in using the library should see
:ref:`install`.

See :ref:`system-requirements` for information regarding supported operating systems, ROCm versions,
and AMD GPUs before building dask-hip.

Environment setup
=================

Create and activate a Conda environment:

.. code-block:: bash

   conda create --name dask-hip python=3.12
   conda activate dask-hip

Alternatively, create a Python virtual environment:

.. code-block:: bash

   python3 -m venv dask-hip-env
   source dask-hip-env/bin/activate

Python dependencies
===================

dask-hip requires the ``amdsmi`` Python package, which is distributed with ROCm (not via AMD
PyPI). Install it from the ROCm installation before building dask-hip. See `AMD SMI documentation <https://rocm.docs.amd.com/projects/amdsmi/en/latest/index.html>`__ for more information.

.. code-block:: bash

   cd /opt/rocm/share/amd_smi
   pip install .

AMD Python packages
-------------------

dask-hip depends on the following AMD-specific Python packages:

- ``hip-python`` -- HIP Python bindings
- ``hip-python-as-cuda`` -- CUDA compatibility layer for HIP
- ``numba-hip`` -- Numba backend for HIP

These are automatically installed when installing from AMD PyPI. When building from source, install
them first:

.. code-block:: bash

   pip install hip-python hip-python-as-cuda numba-hip --extra-index-url=https://pypi.amd.com/rocm-7.2.3/simple/

pynvml compatibility
--------------------

dask-hip bundles a ``pynvml2amdsmi`` compatibility shim that maps ``pynvml`` API calls to their
AMD SMI equivalents, allowing upstream packages such as ``dask.distributed`` to query GPU information
transparently on AMD hardware.

Build and install
=================

Clone the repository and install:

.. code-block:: bash

   git clone https://github.com/ROCm-DS/dask-hip.git
   cd dask-hip
   pip install .

For development (editable) mode:

.. code-block:: bash

   pip install -e .

Running tests
=============

To run the test suite:

.. code-block:: bash

   pip install -e ".[test]"
   pytest dask_cuda/tests/

Building documentation
======================

Install the documentation dependencies:

.. code-block:: bash

   pip install -e ".[docs]"

Build the HTML documentation:

.. code-block:: bash

   cd docs_amd
   sphinx-build -b html . _build

Open ``docs_amd/_build/index.html`` to view the generated documentation.

Regenerating API stubs
-----------------------

The Python API reference is built from ``.pyi`` stub files that are checked into the repository. If
the public API changes (new classes, functions, parameter or docstring updates), regenerate the
stubs on a system with dask-hip and all AMD dependencies installed:

.. code-block:: bash

   pip install mypy                    # provides stubgen
   cd docs_amd/reference/dask_hip_api
   bash generate_stubs.sh

See ``docs_amd/reference/dask_hip_api/README.md`` for details.
