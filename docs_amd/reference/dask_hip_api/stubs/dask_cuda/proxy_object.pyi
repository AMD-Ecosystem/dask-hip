from collections import OrderedDict
from typing import Any, Iterable

from _typeshed import Incomplete

from dask_cuda.disk_io import disk_read as disk_read

from .disk_io import SpillToDiskFile as SpillToDiskFile
from .is_device_object import is_device_object as is_device_object
from .proxify_host_file import ProxyManager as ProxyManager

def asproxy(
    obj: object,
    serializers: Iterable[str] | None = None,
    subclass: type["ProxyObject"] | None = None,
) -> ProxyObject:
    """Wrap ``obj`` in a ProxyObject object if it isn't already.

    Parameters
    ----------
    obj: object
        Object to wrap in a ProxyObject object.
    serializers: Iterable[str], optional
        Serializers to use to serialize ``obj``. If None, no serialization is done.
    subclass: class, optional
        Specify a subclass of ProxyObject to create instead of ProxyObject.
        ``subclass`` must be pickable.

    Returns
    -------
    The ProxyObject proxying ``obj``
    """

def unproxy(obj):
    """Unwrap ProxyObject objects and pass-through anything else.

    Use this function to retrieve the proxied object. Notice, unproxy()
    search through list, tuples, sets, and frozensets.

    Parameters
    ----------
    obj: object
        Any kind of object

    Returns
    -------
    The proxied object or ``obj`` itself if it isn't a ProxyObject
    """

class ProxyManagerDummy:
    """Dummy of a ProxyManager that does nothing

    This is a dummy class used as the manager when no manager has been
    registered the proxy object. It implements dummy methods that doesn't
    do anything it is purely for convenience.
    """

    def add(self, *args, **kwargs) -> None: ...
    def remove(self, *args, **kwargs) -> None: ...
    def maybe_evict(self, *args, **kwargs) -> None: ...
    @property
    def lock(self): ...

class ProxyDetail:
    """Details of a ProxyObject

    In order to avoid having to use thread locks, a ProxyObject maintains
    its state in a ProxyDetail object. The idea is to first make a copy
    of the ProxyDetail object before modifying it and then assign the copy
    back to the ProxyObject in one atomic instruction.

    Parameters
    ----------
    obj: object
        Any kind of object to be proxied.
    fixed_attr: dict
        Dictionary of attributes that are accessible without deserializing
        the proxied object.
    type_serialized: bytes
        Pickled type of ``obj``.
    typename: str
        Name of the type of ``obj``.
    is_cuda_object: boolean
        Whether ``obj`` is a CUDA object or not.
    subclass: bytes
        Pickled type to use instead of ProxyObject when deserializing. The type
        must inherit from ProxyObject.
    serializers: str, optional
        Serializers to use to serialize ``obj``. If None, no serialization is done.
    explicit_proxy: bool
        Mark the proxy object as "explicit", which means that the user allows it
        as input argument to dask tasks even in compatibility-mode.
    manager: ProxyManager or ProxyManagerDummy
        The manager to manage this proxy object or a dummy.
        The manager tallies the total memory usage of proxies and
        evicts/serialize proxy objects as needed.
    """

    obj: Incomplete
    fixed_attr: Incomplete
    type_serialized: Incomplete
    typename: Incomplete
    is_cuda_object: Incomplete
    subclass: Incomplete
    serializer: Incomplete
    explicit_proxy: Incomplete
    manager: Incomplete
    last_access: float
    def __init__(
        self,
        obj: Any,
        fixed_attr: dict[str, Any],
        type_serialized: bytes,
        typename: str,
        is_cuda_object: bool,
        subclass: bytes | None,
        serializer: str | None,
        explicit_proxy: bool,
        manager: ProxyManager | ProxyManagerDummy = ...,
    ) -> None: ...
    def get_init_args(self, include_obj: bool = False) -> OrderedDict:
        """Return the attributes needed to initialize a ProxyObject

        Notice, the returned dictionary is ordered as the __init__() arguments

        Parameters
        ----------
        include_obj: bool
            Whether to include the "obj" argument or not

        Returns
        -------
        Dictionary of attributes
        """
    def is_serialized(self) -> bool:
        """Return whether the proxied object is serialized or not"""
    def serialize(self, serializers: Iterable[str]) -> tuple[dict, list]:
        """Inplace serialization of the proxied object using the ``serializers``

        Parameters
        ----------
        serializers: Iterable[str]
            Serializers to use to serialize the proxied object.

        Returns
        -------
        header: dict
            The header of the serialized frames
        frames: list[bytes]
            List of frames that make up the serialized object
        """
    def deserialize(self, maybe_evict: bool = True, nbytes=None):
        """Inplace deserialization of the proxied object

        Parameters
        ----------
        maybe_evict: bool
            Before deserializing, maybe evict managered proxy objects

        Returns
        -------
        object
            The proxied object (deserialized)
        """

class ProxyObject:
    """Object wrapper/proxy for serializable objects

    This is used by ProxifyHostFile to delay deserialization of returned objects.

    Objects proxied by an instance of this class will be JIT-deserialized when
    accessed. The instance behaves as the proxied object and can be accessed/used
    just like the proxied object.

    ProxyObject has some limitations and doesn't mimic the proxied object perfectly.
    Thus, if encountering problems remember that it is always possible to use unproxy()
    to access the proxied object directly or disable JIT deserialization completely
    with ``jit_unspill=False``.

    Type checking using instance() works as expected but direct type checking
    doesn't:
    >>> import numpy as np
    >>> from dask_cuda.proxy_object import asproxy
    >>> x = np.arange(3)
    >>> isinstance(asproxy(x), type(x))
    True
    >>>  type(asproxy(x)) is type(x)
    False

    Attributes
    ----------
    _pxy: ProxyDetail
        Details of all proxy information of the underlying proxied object.
        Access to _pxy is not pass-through to the proxied object, which is
        the case for most other access to the ProxyObject.

    _pxy_cache: dict
        A dictionary used for caching attributes

    Parameters
    ----------
    detail: ProxyDetail
        The Any kind of object to be proxied.
    """

    def __init__(self, detail: ProxyDetail) -> None: ...
    def __del__(self) -> None:
        """We have to unregister us from the manager if any"""
    def __reduce__(self):
        """Serialization of ProxyObject that uses pickle"""
    def __getattr__(self, name): ...
    def __setattr__(self, name: str, val): ...
    def __array_ufunc__(self, ufunc, method, *args, **kwargs): ...
    def __array_function__(self, func, types, args, kwargs): ...
    @property
    def __class__(self): ...
    def __sizeof__(self) -> int:
        """Returns the size of the proxy object (serialized or not)

        Notice, we cache the result even though the size of proxied object
        when serialized or not serialized might slightly differ.
        """
    def __len__(self) -> int: ...
    def __contains__(self, value) -> bool: ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value) -> None: ...
    def __delitem__(self, key) -> None: ...
    def __getslice__(self, i, j): ...
    def __setslice__(self, i, j, value) -> None: ...
    def __delslice__(self, i, j) -> None: ...
    def __iter__(self): ...
    def __array__(self, *args, **kwargs): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __add__(self, other): ...
    def __sub__(self, other): ...
    def __mul__(self, other): ...
    def __truediv__(self, other): ...
    def __floordiv__(self, other): ...
    def __mod__(self, other): ...
    def __divmod__(self, other): ...
    def __pow__(self, other): ...
    def __lshift__(self, other): ...
    def __rshift__(self, other): ...
    def __and__(self, other): ...
    def __xor__(self, other): ...
    def __or__(self, other): ...
    def __matmul__(self, other): ...
    def __radd__(self, other): ...
    def __rsub__(self, other): ...
    def __rmul__(self, other): ...
    def __rtruediv__(self, other): ...
    def __rfloordiv__(self, other): ...
    def __rmod__(self, other): ...
    def __rdivmod__(self, other): ...
    def __rpow__(self, other, *args): ...
    def __rlshift__(self, other): ...
    def __rrshift__(self, other): ...
    def __rand__(self, other): ...
    def __rxor__(self, other): ...
    def __ror__(self, other): ...
    def __rmatmul__(self, other): ...
    def __iadd__(self, other): ...
    def __isub__(self, other): ...
    def __imul__(self, other): ...
    def __itruediv__(self, other) -> None: ...
    def __ifloordiv__(self, other): ...
    def __imod__(self, other): ...
    def __ipow__(self, other): ...
    def __ilshift__(self, other): ...
    def __irshift__(self, other): ...
    def __iand__(self, other): ...
    def __ixor__(self, other): ...
    def __ior__(self, other): ...
    def __imatmul__(self, other): ...
    def __neg__(self): ...
    def __pos__(self): ...
    def __abs__(self): ...
    def __invert__(self): ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __complex__(self) -> complex: ...
    def __index__(self) -> int: ...

def obj_pxy_is_device_object(obj: ProxyObject):
    """
    In order to avoid de-serializing the proxied object,
    we check ``is_cuda_object`` instead of the default
    ``hasattr(o, "__cuda_array_interface__")`` check.
    """

def handle_disk_serialized(pxy: ProxyDetail):
    """Handle serialization of an already disk serialized proxy

    On a shared filesystem, we do not have to deserialize instead we
    make a hard link of the file.

    On a non-shared filesystem, we deserialize the proxy to host memory.
    """

def obj_pxy_dask_serialize(obj: ProxyObject):
    """The dask serialization of ProxyObject used by Dask when communicating using TCP

    As serializers, it uses "dask" or "pickle", which means that proxied CUDA objects
    are spilled to main memory before communicated. Deserialization is needed, unless
    obj is serialized to disk on a shared filesystem see ``handle_disk_serialized()``.
    """

def obj_pxy_cuda_serialize(obj: ProxyObject):
    """The CUDA serialization of ProxyObject used by Dask when communicating using UCX

    As serializers, it uses "cuda", which means that proxied CUDA objects are _not_
    spilled to main memory before communicated. However, we still have to handle disk
    serialized proxied like in ``obj_pxy_dask_serialize()``
    """

def obj_pxy_dask_deserialize(header, frames):
    """
    The generic deserialization of ProxyObject. Notice, it doesn't deserialize
    the proxied object at this time. When accessed, the proxied object are
    deserialized using the same serializers that were used when the object was
    serialized.
    """

def unproxify_input_wrapper(func):
    """Unproxify the input of ``func``"""

def get_parallel_type_proxy_object(obj: ProxyObject): ...
