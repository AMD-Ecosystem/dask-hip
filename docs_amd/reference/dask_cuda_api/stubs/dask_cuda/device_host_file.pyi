from _typeshed import Incomplete
from zict import Buffer
from zict.common import ZictBase

from .is_device_object import is_device_object as is_device_object
from .is_spillable_object import is_spillable_object as is_spillable_object
from .utils import nvtx_annotate as nvtx_annotate

class LoggedBuffer(Buffer):
    """Extends zict.Buffer with logging capabilities

    Two arguments ``fast_name`` and ``slow_name`` are passed to constructor that
    identify a user-friendly name for logging of where spilling is going from/to.
    For example, their names can be "Device" and "Host" to identify that spilling
    is happening from a CUDA device into system memory.
    """

    addr: Incomplete
    fast_name: Incomplete
    slow_name: Incomplete
    msg_template: str
    logger: Incomplete
    total_time_fast_to_slow: float
    total_time_slow_to_fast: float
    def __init__(
        self,
        *args,
        fast_name: str = "Fast",
        slow_name: str = "Slow",
        addr=None,
        **kwargs
    ) -> None: ...
    def fast_to_slow(self, key, value): ...
    def slow_to_fast(self, key): ...
    def set_address(self, addr) -> None: ...
    def get_total_spilling_time(self): ...

class DeviceSerialized:
    """Store device object on the host

    This stores a device-side object as
    1.  A msgpack encodable header
    2.  A list of ``bytes``-like objects (like NumPy arrays)
        that are in host memory
    """

    header: Incomplete
    frames: Incomplete
    def __init__(self, header, frames) -> None: ...
    def __sizeof__(self) -> int: ...
    def __reduce_ex__(self, protocol): ...

def device_serialize(obj): ...
def device_deserialize(header, frames): ...
def device_to_host(obj: object) -> DeviceSerialized: ...
def host_to_device(s: DeviceSerialized) -> object: ...

class DeviceHostFile(ZictBase):
    """Manages serialization/deserialization of objects.

    Three LRU cache levels are controlled, for device, host and disk.
    Each level takes care of serializing objects once its limit has been
    reached and pass it to the subsequent level. Similarly, each cache
    may deserialize the object, but storing it back in the appropriate
    cache, depending on the type of object being deserialized.

    Parameters
    ----------
    worker_local_directory: path
        Path where to store serialized objects on disk
    device_memory_limit: int or None
        Number of bytes of CUDA device memory for device LRU cache,
        spills to host cache once filled. Setting this ``0`` or ``None``
        means unlimited device memory, implies no spilling to host.
    memory_limit: int or None
        Number of bytes of host memory for host LRU cache, spills to
        disk once filled. Setting this to ``0`` or ``None`` means unlimited
        host memory, implies no spilling to disk.
    log_spilling: bool
        If True, all spilling operations will be logged directly to
        distributed.worker with an INFO loglevel. This will eventually be
        replaced by a Dask configuration flag.
    """

    disk_func_path: Incomplete
    host_func: Incomplete
    disk_func: Incomplete
    host_buffer: Incomplete
    device_keys: Incomplete
    device_func: Incomplete
    device_host_func: Incomplete
    device_buffer: Incomplete
    device: Incomplete
    host: Incomplete
    disk: Incomplete
    fast: Incomplete
    others: Incomplete
    def __init__(
        self,
        worker_local_directory,
        *,
        device_memory_limit=None,
        memory_limit=None,
        log_spilling: bool = False
    ) -> None: ...
    def __setitem__(self, key, value) -> None: ...
    def __getitem__(self, key): ...
    def __len__(self) -> int: ...
    def __iter__(self): ...
    def __delitem__(self, key) -> None: ...
    def evict(self):
        """Evicts least recently used host buffer (aka, CPU or system memory)

        Implements distributed.spill.ManualEvictProto interface"""
    def set_address(self, addr) -> None: ...
    def get_total_spilling_time(self): ...
