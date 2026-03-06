Query an existing GPU cluster's configuration.

A cluster can be specified either through a URI passed through the ``SCHEDULER``
argument or a scheduler file passed through the ``--scheduler-file`` option.

.. program:: dask cuda config
.. rubric:: Usage

.. code-block:: shell

    dask cuda config [OPTIONS] [SCHEDULER] [PRELOAD_ARGV]...

.. rubric:: Options

.. option:: --scheduler-file <scheduler_file>

    Filename to JSON encoded scheduler information. To be used in conjunction
    with the equivalent ``dask scheduler`` option.

.. option:: --tls-ca-file <tls_ca_file>

    CA certificate(s) file for TLS (in PEM format). Can be a string (like
    ``"path/to/certs"``), or ``None`` for no certificate(s).

.. option:: --tls-cert <tls_cert>

    Certificate file for TLS (in PEM format). Can be a string (like
    ``"path/to/certs"``), or ``None`` for no certificate(s).

.. option:: --tls-key <tls_key>

    Private key file for TLS (in PEM format). Can be a string (like
    ``"path/to/certs"``), or ``None`` for no private key.

.. rubric:: Arguments

.. option:: SCHEDULER

    Optional argument

.. option:: PRELOAD_ARGV

    Optional argument(s)
