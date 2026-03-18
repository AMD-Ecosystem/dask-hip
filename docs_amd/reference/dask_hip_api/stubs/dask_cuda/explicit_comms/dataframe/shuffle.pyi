from typing import Any, Callable, TypeVar

import dask_expr

from dask.dataframe import DataFrame as DataFrame, Series as Series
from distributed.worker import Worker as Worker

from ..._compat import DASK_2025_4_0 as DASK_2025_4_0
from .. import comms as comms

T = TypeVar("T")
Proxify = Callable[[T], T]

def get_proxify(worker: Worker) -> Proxify:
    """Get function to proxify objects"""

def get_no_comm_postprocess(
    stage: dict[str, Any], num_rounds: int, batchsize: int, proxify: Proxify
) -> Callable[[DataFrame], DataFrame]:
    """Get function for post-processing partitions not communicated

    In cuDF, the ``group_split_dispatch`` uses ``scatter_by_map`` to create
    the partitions, which is implemented by splitting a single base dataframe
    into multiple partitions. This means that memory are not freed until
    ALL partitions are deleted.

    In order to free memory ASAP, we can deep copy partitions NOT being
    communicated. We do this when ``num_rounds != batchsize``.

    Parameters
    ----------
    stage
        The staged input dataframes.
    num_rounds
        Number of rounds of dataframe partitioning and all-to-all communication.
    batchsize
        Number of partitions each worker will handle in each round.
    proxify
        Function to proxify object.

    Returns
    -------
    Function to be called on partitions not communicated.

    """

async def send(
    eps,
    myrank: int,
    rank_to_out_part_ids: dict[int, set[int]],
    out_part_id_to_dataframe: dict[int, DataFrame],
) -> None:
    """Notice, items sent are removed from ``out_part_id_to_dataframe``"""

async def recv(
    eps,
    myrank: int,
    rank_to_out_part_ids: dict[int, set[int]],
    out_part_id_to_dataframe_list: dict[int, list[DataFrame]],
    proxify: Proxify,
) -> None:
    """Notice, received items are appended to ``out_parts_list``"""

def compute_map_index(
    df: DataFrame, column_names: list[str], npartitions: int
) -> Series:
    """Return a Series that maps each row ``df`` to a partition ID

    The partitions are determined by hashing the columns given by column_names
    unless if ``column_names[0] == "_partitions"``, in which case the values of
    ``column_names[0]`` are used as index.

    Parameters
    ----------
    df
        The dataframe.
    column_names
        List of column names on which we want to split.
    npartitions
        The desired number of output partitions.

    Returns
    -------
    Series
        Series that maps each row ``df`` to a partition ID
    """

def partition_dataframe(
    df: DataFrame, column_names: list[str], npartitions: int, ignore_index: bool
) -> dict[int, DataFrame]:
    """Partition dataframe to a dict of dataframes

    The partitions are determined by hashing the columns given by column_names
    unless ``column_names[0] == "_partitions"``, in which case the values of
    ``column_names[0]`` are used as index.

    Parameters
    ----------
    df
        The dataframe to partition
    column_names
        List of column names on which we want to partition.
    npartitions
        The desired number of output partitions.
    ignore_index
        Ignore index during shuffle. If True, performance may improve,
        but index values will not be preserved.

    Returns
    -------
    partitions
        Dict of dataframe-partitions, mapping partition-ID to dataframe
    """

def create_partitions(
    stage: dict[str, Any],
    batchsize: int,
    column_names: list[str],
    npartitions: int,
    ignore_index: bool,
    proxify: Proxify,
) -> dict[int, DataFrame]:
    """Create partitions from one or more staged dataframes

    Parameters
    ----------
    stage
        The staged input dataframes
    column_names
        List of column names on which we want to split.
    npartitions
        The desired number of output partitions.
    ignore_index
        Ignore index during shuffle.  If True, performance may improve,
        but index values will not be preserved.
    proxify
        Function to proxify object.

    Returns
    -------
    partitions: list of DataFrames
        List of dataframe-partitions
    """

async def send_recv_partitions(
    eps: dict,
    myrank: int,
    rank_to_out_part_ids: dict[int, set[int]],
    out_part_id_to_dataframe: dict[int, DataFrame],
    no_comm_postprocess: Callable[[DataFrame], DataFrame],
    proxify: Proxify,
    out_part_id_to_dataframe_list: dict[int, list[DataFrame]],
) -> None:
    """Send and receive (all-to-all) partitions between all workers

    Parameters
    ----------
    eps
        Communication endpoints to the other workers.
    myrank
        The rank of this worker.
    rank_to_out_part_ids
        dict that for each worker rank specifies a set of output partition IDs.
        If the worker shouldn't return any partitions, it is excluded from the
        dict. Partition IDs are global integers ``0..npartitions`` and corresponds
        to the dict keys returned by ``group_split_dispatch``.
    out_part_id_to_dataframe
        Mapping from partition ID to dataframe. This dict is cleared on return.
    no_comm_postprocess
        Function to post-process partitions not communicated.
        See ``get_no_comm_postprocess``
    proxify
        Function to proxify object.
    out_part_id_to_dataframe_list
        The **output** of this function, which is a dict of the partitions owned by
        this worker.
    """

async def shuffle_task(
    s,
    stage_name: str,
    rank_to_inkeys: dict[int, set],
    rank_to_out_part_ids: dict[int, set[int]],
    column_names: list[str],
    npartitions: int,
    ignore_index: bool,
    num_rounds: int,
    batchsize: int,
) -> dict[int, DataFrame]:
    """Explicit-comms shuffle task

    This function is running on each worker participating in the shuffle.

    Parameters
    ----------
    s: dict
        Worker session state
    stage_name: str
        Name of the stage to retrieve the input keys from.
    rank_to_inkeys: dict
        dict that for each worker rank specifies the set of staged input keys.
    rank_to_out_part_ids: dict
        dict that for each worker rank specifies a set of output partition IDs.
        If the worker shouldn't return any partitions, it is excluded from the
        dict. Partition IDs are global integers ``0..npartitions`` and corresponds
        to the dict keys returned by ``group_split_dispatch``.
    column_names: list of strings
        List of column names on which we want to split.
    npartitions: int
        The desired number of output partitions.
    ignore_index: bool
        Ignore index during shuffle.  If True, performance may improve,
        but index values will not be preserved.
    num_rounds: int
        Number of rounds of dataframe partitioning and all-to-all communication.
    batchsize: int
        Number of partitions each worker will handle in each round.

    Returns
    -------
    partitions: dict
        dict that maps each Partition ID to a dataframe-partition
    """

def shuffle(
    df: DataFrame,
    column_names: list[str],
    npartitions: int | None = None,
    ignore_index: bool = False,
    batchsize: int | None = None,
) -> DataFrame:
    """Order divisions of DataFrame so that all values within column(s) align

    This enacts a task-based shuffle using explicit-comms. It requires a full
    dataset read, serialization and shuffle. This is expensive. If possible
    you should avoid shuffles.

    This does not preserve a meaningful index/partitioning scheme. This is not
    deterministic if done in parallel.

    Requires an activate client.

    Parameters
    ----------
    df: dask.dataframe.DataFrame
        Dataframe to shuffle
    column_names: list of strings
        List of column names on which we want to split.
    npartitions: int or None
        The desired number of output partitions. If None, the number of output
        partitions equals ``df.npartitions``
    ignore_index: bool
        Ignore index during shuffle. If True, performance may improve,
        but index values will not be preserved.
    batchsize: int
        A shuffle consist of multiple rounds where each worker partitions and
        then all-to-all communicates a number of its dataframe partitions. The batch
        size is the number of partitions each worker will handle in each round.
        If -1, each worker will handle all its partitions in a single round and
        all techniques to reduce memory usage are disabled, which might be faster
        when memory pressure isn't an issue.
        If None, the value of ``DASK_EXPLICIT_COMMS_BATCHSIZE`` is used or 1 if not
        set thus by default, we prioritize robustness over performance.

    Returns
    -------
    df: dask.dataframe.DataFrame
        Shuffled dataframe

    Developer Notes
    ---------------
    The implementation consist of three steps:
      (a) Stage the partitions of ``df`` on all workers and then cancel them
          thus at this point the Dask Scheduler doesn't know about any of the
          the partitions.
      (b) Submit a task on each worker that shuffle (all-to-all communicate)
          the staged partitions and return a list of dataframe-partitions.
      (c) Submit a dask graph that extract (using ``getitem()``) individual
          dataframe-partitions from (b).
    """

class ECShuffle(dask_expr._shuffle.TaskShuffle):
    """Explicit-Comms Shuffle Expression."""

def patch_shuffle_expression() -> None:
    """Patch Dasks Shuffle expression.

    Notice, this is monkey patched into Dask at dask_cuda
    import, and it changes ``Shuffle._layer`` to lower into
    an ``ECShuffle`` expression when the 'explicit-comms'
    config is set to ``True``.
    """
