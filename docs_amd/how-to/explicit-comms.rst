.. SPDX-FileCopyrightText: Copyright (c) 2026 Advanced Micro Devices, Inc.
.. SPDX-License-Identifier: MIT

.. meta::
   :description: dask-hip explicit communication guide
   :keywords: Dask, GPU, explicit communication, shuffle, HIP, ROCm, ROCm-DS, AMD

.. _explicit-comms:

**********************
Explicit communication
**********************

Communication and scheduling overhead can be a major bottleneck in Dask/Distributed. ``dask-hip`` addresses this by introducing an API for explicit communication in Dask tasks. The idea is that Dask/Distributed spawns workers and distributes data as usual while the user can submit tasks on the workers that communicate explicitly.

This makes it possible to bypass Distributed's scheduler and write hand-tuned computation and communication patterns. Currently, ``dask-hip`` includes an explicit-comms implementation of the DataFrame shuffle operation used for merging and sorting.

Usage
=====

To use explicit-comms in Dask/Distributed automatically, define the environment variable ``DASK_EXPLICIT_COMMS=True`` or set the ``"explicit-comms"`` key in the `Dask configuration <https://docs.dask.org/en/latest/configuration.html>`_:

.. code-block:: python

   import dask

   with dask.config.set({"explicit-comms": True}):
       # DataFrame operations that use shuffle (merge, sort)
       # will automatically use explicit communication
       result = df.merge(other_df, on="key")

It is also possible to use explicit-comms in tasks manually. See the :doc:`API reference <../reference/api>` for ``CommsContext`` and ``shuffle``.
