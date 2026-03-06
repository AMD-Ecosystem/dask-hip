import os
import pathlib
import tempfile
from typing import Callable, Iterable, Mapping

from _typeshed import Incomplete

def get_new_cuda_buffer() -> Callable[[int], object]:
    """Return a function to create an empty CUDA buffer"""

class SpillToDiskFile:
    """File path the gets removed on destruction

    When spilling to disk, we have to delay the removal of the file
    until no more proxies are pointing to the file.
    """

    path: str
    def __init__(self, path: str) -> None: ...
    def __del__(self) -> None: ...
    def exists(self): ...
    def __deepcopy__(self, memo) -> str:
        """A deep copy is simply the path as a string.

        In order to avoid multiple instance of SpillToDiskFile pointing
        to the same file, we do not allow a direct copy.
        """
    def __copy__(self) -> None: ...
    def __reduce__(self) -> None: ...

class SpillToDiskProperties:
    gds_enabled: bool
    shared_filesystem: bool
    root_dir: pathlib.Path
    tmpdir: tempfile.TemporaryDirectory
    lock: Incomplete
    counter: int
    def __init__(
        self,
        root_dir: str | os.PathLike,
        shared_filesystem: bool | None = None,
        gds: bool | None = None,
    ) -> None:
        """
        Parameters
        ----------
        root_dir : os.PathLike
            Path to the root directory to write serialized data.
        shared_filesystem: bool or None, default None
            Whether the ``root_dir`` above is shared between all workers or not.
            If ``None``, the "jit-unspill-shared-fs" config value are used, which
            defaults to False.
        gds: bool
            Enable the use of GPUDirect Storage. If ``None``, the "gds-spilling"
            config value are used, which defaults to ``False``.
        """
    def gen_file_path(self) -> str:
        """Generate an unique file path"""

def disk_write(
    path: str, frames: Iterable, shared_filesystem: bool, gds: bool = False
) -> dict:
    """Write frames to disk

    Parameters
    ----------
    path: str
        File path
    frames: Iterable
        The frames to write to disk
    shared_filesystem: bool
        Whether the target filesystem is shared between all workers or not.
        If True, the filesystem must support the ``os.link()`` operation.
    gds: bool
        Enable the use of GPUDirect Storage. Notice, the consecutive
        ``disk_read()`` must enable GDS as well.

    Returns
    -------
    header: dict
        A dict of metadata
    """

def disk_read(header: Mapping, gds: bool = False) -> list:
    """Read frames from disk

    Parameters
    ----------
    header: Mapping
        The metadata of the frames to read
    gds: bool
        Enable the use of GPUDirect Storage. Notice, this must
        match the GDS option set by the prior ``disk_write()`` call.

    Returns
    -------
    frames: list
        List of read frames
    """
