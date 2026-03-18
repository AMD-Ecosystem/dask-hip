import abc
from collections.abc import MutableMapping
from typing import Any, Callable, DefaultDict, Hashable, Iterable, TypeVar

from _typeshed import Incomplete

from .disk_io import (
    SpillToDiskProperties as SpillToDiskProperties,
    disk_read as disk_read,
    disk_write as disk_write,
)
from .get_device_memory_objects import (
    DeviceMemoryId as DeviceMemoryId,
    get_device_memory_ids as get_device_memory_ids,
)
from .is_spillable_object import cudf_spilling_status as cudf_spilling_status
from .proxify_device_objects import (
    proxify_device_objects as proxify_device_objects,
    unproxify_device_objects as unproxify_device_objects,
)
from .proxy_object import ProxyObject as ProxyObject
from .utils import get_rmm_device_memory_usage as get_rmm_device_memory_usage

T = TypeVar("T")

class Proxies(abc.ABC, metaclass=abc.ABCMeta):
    """Abstract base class to implement tracking of proxies

    This class is not threadsafe
    """

    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    @abc.abstractmethod
    def mem_usage_add(self, proxy: ProxyObject) -> None:
        """Given a new proxy, update ``self._mem_usage``"""
    @abc.abstractmethod
    def mem_usage_remove(self, proxy: ProxyObject) -> None:
        """Removal of proxy, update ``self._mem_usage``"""
    @abc.abstractmethod
    def buffer_info(self) -> list[tuple[float, int, list[ProxyObject]]]:
        """Return a list of buffer information

        The returned format is:
            ``[(<access-time>, <size-of-buffer>, <list-of-proxies>), ...]``
        """
    def add(self, proxy: ProxyObject) -> None:
        """Add a proxy for tracking, calls ``self.mem_usage_add``"""
    def remove(self, proxy: ProxyObject) -> None:
        """Remove proxy from tracking, calls ``self.mem_usage_remove``"""
    def get_proxies(self) -> list[ProxyObject]:
        """Return a list of all proxies"""
    def get_proxies_by_ids(self, proxy_ids: Iterable[int]) -> list[ProxyObject]:
        """Return a list of proxies"""
    def contains_proxy_id(self, proxy_id: int) -> bool: ...
    def mem_usage(self) -> int: ...

class ProxiesOnHost(Proxies):
    """Implement tracking of proxies on the CPU

    This uses dask.sizeof to update memory usage.
    """

    def mem_usage_add(self, proxy: ProxyObject) -> None: ...
    def mem_usage_remove(self, proxy: ProxyObject) -> None: ...
    def buffer_info(self) -> list[tuple[float, int, list[ProxyObject]]]: ...

class ProxiesOnDisk(ProxiesOnHost):
    """Implement tracking of proxies on the Disk"""

class ProxiesOnDevice(Proxies):
    """Implement tracking of proxies on the GPU

    This is a bit more complicated than ProxiesOnHost because we have to
    handle that multiple proxy objects can refer to the same underlying
    device memory object. Thus, we have to track aliasing and make sure
    we don't count down the memory usage prematurely.

    Notice, we only track direct aliasing thus multiple proxy objects can
    point to different non-overlapping parts of the same device buffer.
    In this case the tally of the total device memory usage is incorrect.
    """

    proxy_id_to_dev_mems: dict[int, set[DeviceMemoryId]]
    dev_mem_to_proxy_ids: DefaultDict[DeviceMemoryId, set[int]]
    def __init__(self) -> None: ...
    def mem_usage_add(self, proxy: ProxyObject) -> None: ...
    def mem_usage_remove(self, proxy: ProxyObject) -> None: ...
    def buffer_info(self) -> list[tuple[float, int, list[ProxyObject]]]: ...

class ProxyManager:
    """
    This class together with Proxies, ProxiesOnHost, and ProxiesOnDevice
    implements the tracking of all known proxies and their total host/device
    memory usage. It turns out having to re-calculate memory usage continuously
    is too expensive.

    The idea is to have the ProxifyHostFile or the proxies themselves update
    their location (device or host). The manager then tallies the total memory usage.

    Notice, the manager only keeps weak references to the proxies.
    """

    lock: Incomplete
    def __init__(self, device_memory_limit: int, memory_limit: int) -> None: ...
    def __len__(self) -> int: ...
    def pprint(self) -> str: ...
    def get_proxies_by_serializer(self, serializer: str | None) -> Proxies:
        """Get Proxies collection by serializer"""
    def get_proxies_by_proxy_object(self, proxy: ProxyObject) -> Proxies | None:
        """Get Proxies collection by proxy object"""
    def contains(self, proxy_id: int) -> bool:
        """Is the proxy in any of the Proxies collection?"""
    def add(self, proxy: ProxyObject, serializer: str | None) -> None:
        """Add the proxy to the Proxies collection by that match the serializer"""
    def remove(self, proxy: ProxyObject) -> None:
        """Remove the proxy from the Proxies collection it is in"""
    def validate(self) -> None:
        """Validate the state of the manager"""
    def proxify(self, obj: T, duplicate_check: bool = True) -> tuple[T, bool]:
        """Proxify ``obj`` and add found proxies to the ``Proxies`` collections

        Search through ``obj`` and wrap all CUDA device objects in ProxyObject.
        If duplicate_check is True, identical CUDA device objects found in
        ``obj`` are wrapped by the same ProxyObject.

        Returns the proxified object and a boolean, which is ``True`` when one or
        more incompatible-types were found.

        Parameters
        ----------
        obj
            Object to search through or wrap in a ProxyObject.
        duplicate_check
            Make sure that identical CUDA device objects found in ``obj`` are
            wrapped by the same ProxyObject. This check comes with a significant
            overhead hence it is recommended setting to False when it is known
            that no duplicate exist.

        Return
        ------
        obj
            The proxified object.
        bool
            Whether incompatible-types were found or not.
        """
    def evict(
        self,
        nbytes: int,
        proxies_access: Callable[[], list[tuple[float, int, list[ProxyObject]]]],
        serializer: Callable[[ProxyObject], None],
    ) -> int:
        """Evict buffers retrieved by calling ``proxies_access``

        Calls ``proxies_access`` to retrieve a list of proxies and then spills
        enough proxies to free up at a minimum ``nbytes`` bytes. In order to
        spill a proxy, ``serializer`` is called.

        Parameters
        ----------
        nbytes: int
            Number of bytes to evict.
        proxies_access: callable
            Function that returns a list of proxies pack in a tuple like:
            ``[(<access-time>, <size-of-buffer>, <list-of-proxies>), ...]``
        serializer: callable
            Function that serialize the given proxy object.

        Return
        ------
        nbytes: int
            Number of bytes spilled.
        """
    def maybe_evict_from_device(self, extra_dev_mem: int = 0) -> None:
        """Evict buffers until total memory usage is below device-memory-limit

        Adds ``extra_dev_mem`` to the current total memory usage when comparing
        against device-memory-limit.
        """
    def maybe_evict_from_host(self, extra_host_mem: int = 0) -> None:
        """Evict buffers until total memory usage is below host-memory-limit

        Adds ``extra_host_mem`` to the current total memory usage when comparing
        against device-memory-limit.
        """
    def maybe_evict(self, extra_dev_mem: int = 0) -> None: ...

class ProxifyHostFile(MutableMapping):
    """Host file that proxify stored data

    This class is an alternative to the default disk-backed LRU dict used by
    workers in Distributed.

    It wraps all CUDA device objects in a ProxyObject instance and maintains
    ``device_memory_limit`` by spilling ProxyObject on-the-fly. This addresses
    some issues with the default DeviceHostFile host, which tracks device
    memory inaccurately see <https://github.com/rapidsai/dask-cuda/pull/451>

    Limitations
    -----------
    - For now, ProxifyHostFile doesn\'t support spilling to disk.
    - ProxyObject has some limitations and doesn\'t mimic the proxied object
      perfectly. See docs of ProxyObject for detail.
    - This is still experimental, expect bugs and API changes.

    Parameters
    ----------
    worker_local_directory: str
        Path on local machine to store temporary files.
        WARNING, this **cannot** change while running thus all serialization to
        disk are using the same directory.
    device_memory_limit: int
        Number of bytes of CUDA device memory used before spilling to host.
    memory_limit: int
        Number of bytes of host memory used before spilling to disk.
    shared_filesystem: bool or None, default None
        Whether the ``local_directory`` above is shared between all workers or not.
        If ``None``, the "jit-unspill-shared-fs" config value are used, which
        defaults to False.
        Notice, a shared filesystem must support the ``os.link()`` operation.
    compatibility_mode: bool or None, default None
        Enables compatibility-mode, which means that items are un-proxified before
        retrieval. This makes it possible to get some of the JIT-unspill benefits
        without having to be ProxyObject compatible. In order to still allow specific
        ProxyObjects, set the ``mark_as_explicit_proxies=True`` when proxifying with
        ``proxify_device_objects()``. If ``None``, the "jit-unspill-compatibility-mode"
        config value are used, which defaults to False.
    spill_on_demand: bool or None, default None
        Enables spilling when the RMM memory pool goes out of memory. If ``None``,
        the "spill-on-demand" config value are used, which defaults to True.
        Notice, enabling this does nothing when RMM isn\'t available or not used.
    gds_spilling: bool
        Enable GPUDirect Storage spilling. If ``None``, the "gds-spilling" config
        value are used, which defaults to ``False``.
    """

    lock: Incomplete
    store: dict[Hashable, tuple[Any, bool]]
    manager: Incomplete
    compatibility_mode: Incomplete
    spill_on_demand_initialized: Incomplete
    logger: Incomplete
    def __init__(
        self,
        worker_local_directory: str,
        *,
        device_memory_limit: int,
        memory_limit: int,
        shared_filesystem: bool | None = None,
        compatibility_mode: bool | None = None,
        spill_on_demand: bool | None = None,
        gds_spilling: bool | None = None
    ) -> None: ...
    def __contains__(self, key) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self): ...
    def initialize_spill_on_demand_once(self):
        """Register callback function to handle RMM out-of-memory exceptions

        This function is idempotent and should be called at least once. Currently, we
        do this in __setitem__ instead of in __init__ because a Dask worker might re-
        initiate the RMM pool and its resource adaptors after creating ProxifyHostFile.
        """
    def evict(self) -> int:
        """Manually evict 1% of host limit.

        Dask uses this to trigger CPU-to-Disk spilling. We don't know how much
        we need to spill but Dask will call ``evict()`` repeatedly until enough
        is spilled. We ask for 1% each time.

        Return
        ------
        nbytes: int
            Number of bytes spilled or -1 if nothing to spill.
        """
    @property
    def fast(self):
        """Alternative access to ``.evict()`` used by Dask

        Dask expects ``.fast.evict()`` to be available for manually triggering
        of CPU-to-Disk spilling.
        """
    def __setitem__(self, key, value) -> None: ...
    def __getitem__(self, key): ...
    def __delitem__(self, key) -> None: ...
    @classmethod
    def register_disk_spilling(cls) -> None:
        """Register Dask serializers that writes to disk

        This is a static method because the registration of a Dask
        serializer/deserializer pair is a global operation thus we can
        only register one such pair. This means that all instances of
        the ``ProxifyHostFile`` end up using the same ``local_directory``.
        """
    @classmethod
    def serialize_proxy_to_disk_inplace(cls, proxy: ProxyObject) -> None:
        """Serialize ``proxy`` to disk.

        Avoid de-serializing if ``proxy`` is serialized using "dask" or
        "pickle". In this case the already serialized data is written
        directly to disk.

        Parameters
        ----------
        proxy : ProxyObject
            Proxy object to serialize using the "disk" serialize.
        """
