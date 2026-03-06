from typing import Any, Hashable, Iterable

from _typeshed import Incomplete

from distributed import Client as Client, Worker as Worker

def get_multi_lock_or_null_context(multi_lock_context, *args, **kwargs):
    """Return either a MultiLock or a NULL context

    Parameters
    ----------
    multi_lock_context: bool
        If True return MultiLock context else return a NULL context that
        doesn't do anything

    *args, **kwargs:
        Arguments parsed to the MultiLock creation

    Returns
    -------
    context: context
        Either ``MultiLock(*args, **kwargs)`` or a NULL context
    """

def default_comms(client: Client | None = None) -> CommsContext:
    """Return the default comms object for ``client``.

    Creates a new default comms object if one does not already exist
    for ``client``.

    Parameters
    ----------
    client: Client, optional
        If no default comm object exists, create the new comm on ``client``
        are returned.

    Returns
    -------
    comms: CommsContext
        The default comms object

    Notes
    -----
    There are some subtle points around explicit-comms and the lifecycle
    of a Dask Cluster.

    A :class:`CommsContext` establishes explicit communication channels
    between the workers *at the time it's created*. If workers are added
    or removed, they will not be included in the communication channels
    with the other workers.

    If you need to refresh the explicit communications channels, then
    create a new :class:`CommsContext` object or call ``default_comms``
    again after workers have been added to or removed from the cluster.
    """

def worker_state(sessionId: int | None = None) -> dict:
    """Retrieve the state(s) of the current worker

    Parameters
    ----------
    sessionId: int, optional
        Worker session state ID. If None, all states of the worker
        are returned.

    Returns
    -------
    state: dict
        Either a single state dict or a dict of state dict
    """

class CommsContext:
    """Communication handler for explicit communication

    Parameters
    ----------
    client: Client, optional
        Specify client to use for communication. If None, use the default client.
    """

    client: Client
    sessionId: int
    worker_addresses: list[str]
    worker_direct_addresses: Incomplete
    def __init__(self, client: Client | None = None) -> None: ...
    def submit(self, worker, coroutine, *args, wait: bool = False):
        """Run a coroutine on a single worker

        The coroutine is given the worker's state dict as the first argument
        and ``*args`` as the following arguments.

        Parameters
        ----------
        worker: str
            Worker to run the ``coroutine``
        coroutine: coroutine
            The function to run on the worker
        *args:
            Arguments for ``coroutine``
        wait: boolean, optional
            If True, waits for the coroutine to finished before returning.

        Returns
        -------
        ret: object or Future
            If wait=True, the result of ``coroutine``
            If wait=False, Future that can be waited on later.
        """
    def run(self, coroutine, *args, workers=None, lock_workers: bool = False):
        """Run a coroutine on multiple workers

        The coroutine is given the worker's state dict as the first argument
        and ``*args`` as the following arguments.

        Parameters
        ----------
        coroutine: coroutine
            The function to run on each worker
        *args:
            Arguments for ``coroutine``
        workers: list, optional
            List of workers. Default is all workers
        lock_workers: bool, optional
            Use distributed.MultiLock to get exclusive access to the workers. Use
            this flag to support parallel runs.

        Returns
        -------
        ret: list
            List of the output from each worker
        """
    def stage_keys(self, name: str, keys: Iterable[Hashable]) -> dict[int, set]:
        """Staging keys on workers under the given name

        In an explicit-comms task, use ``pop_staging_area(..., name)`` to access
        the staged keys and the associated data.

        Notes
        -----
        In the context of explicit-comms, staging is the act of duplicating the
        responsibility of Dask keys. When staging a key, the worker owning the
        key (as assigned by the Dask scheduler) save a reference to the key and
        the associated data to its local staging area. From this point on, if
        the scheduler cancels the key, the worker (and the task running on the
        worker) now has exclusive access to the key and the associated data.
        This way, staging makes it possible for long running explicit-comms tasks
        to free input data ASAP.

        Parameters
        ----------
        name: str
            Name for the staging area
        keys: iterable
            The keys to stage

        Returns
        -------
        dict
            dict that maps each worker-rank to the workers set of staged keys
        """

def pop_staging_area(session_state: dict, name: str) -> dict[str, Any]:
    """Pop the staging area called ``name``

    This function must be called within a running explicit-comms task.

    Parameters
    ----------
    session_state: dict
        Worker session state
    name: str
        Name for the staging area

    Returns
    -------
    dict
        The staging area, which is a dict that maps keys to their data.
    """
