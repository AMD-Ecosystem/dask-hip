from typing import MutableMapping, TypeVar

from _typeshed import Incomplete

from .proxy_object import ProxyObject as ProxyObject, asproxy as asproxy

dispatch: Incomplete
incompatible_types: tuple[type] | None
T = TypeVar("T")

def proxify_device_objects(
    obj: T,
    proxied_id_to_proxy: MutableMapping[int, ProxyObject] | None = None,
    found_proxies: list[ProxyObject] | None = None,
    excl_proxies: bool = False,
    mark_as_explicit_proxies: bool = False,
) -> T:
    """Wrap device objects in ProxyObject

    Search through ``obj`` and wraps all CUDA device objects in ProxyObject.
    It uses ``proxied_id_to_proxy`` to make sure that identical CUDA device
    objects found in ``obj`` are wrapped by the same ProxyObject.

    Parameters
    ----------
    obj: Any
        Object to search through or wrap in a ProxyObject.
    proxied_id_to_proxy: MutableMapping[int, ProxyObject]
        Dict mapping the id() of proxied objects (CUDA device objects) to
        their proxy and is updated with all new proxied objects found in ``obj``.
        If None, use an empty dict.
    found_proxies: List[ProxyObject]
        List of found proxies in ``obj``. Notice, this includes all proxies found,
        including those already in ``proxied_id_to_proxy``.
        If None, use an empty list.
    excl_proxies: bool
        Don\'t add found objects that are already ProxyObject to found_proxies.
    mark_as_explicit_proxies: bool
        Mark found proxies as "explicit", which means that the user allows them
        as input arguments to dask tasks even in compatibility-mode.

    Returns
    -------
    ret: Any
        A copy of ``obj`` where all CUDA device objects are wrapped in ProxyObject
    """

def unproxify_device_objects(
    obj: T, skip_explicit_proxies: bool = False, only_incompatible_types: bool = False
) -> T:
    """Unproxify device objects

    Search through ``obj`` and un-wraps all CUDA device objects.

    Parameters
    ----------
    obj: Any
        Object to search through or unproxify.
    skip_explicit_proxies: bool
        When True, skipping proxy objects marked as explicit proxies.
    only_incompatible_types: bool
        When True, ONLY unproxify incompatible type. The skip_explicit_proxies
        argument is ignored.

    Returns
    -------
    ret: Any
        A copy of ``obj`` where all CUDA device objects are unproxify
    """

def proxify_decorator(func):
    """Returns a function wrapper that explicit proxify the output

    Notice, this function only has effect in compatibility mode.
    """

def unproxify_decorator(func):
    """Returns a function wrapper that unproxify output

    Notice, this function only has effect in compatibility mode.
    """

def proxify(obj, proxied_id_to_proxy, found_proxies, subclass=None): ...
def proxify_device_object_default(
    obj, proxied_id_to_proxy, found_proxies, excl_proxies
): ...
def proxify_device_object_proxy_object(
    obj: ProxyObject, proxied_id_to_proxy, found_proxies, excl_proxies
): ...
def proxify_device_object_python_collection(
    seq, proxied_id_to_proxy, found_proxies, excl_proxies
): ...
def proxify_device_object_python_dict(
    seq, proxied_id_to_proxy, found_proxies, excl_proxies
): ...
