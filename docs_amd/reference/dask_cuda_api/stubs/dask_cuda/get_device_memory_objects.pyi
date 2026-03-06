from _typeshed import Incomplete

dispatch: Incomplete

class DeviceMemoryId:
    """ID and size of device memory objects

    Instead of keeping a reference to device memory objects this class
    only saves the id and size in order to avoid delayed freeing.
    """

    id: Incomplete
    nbytes: Incomplete
    def __init__(self, obj: object) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, o) -> bool: ...

def get_device_memory_ids(obj) -> set[DeviceMemoryId]:
    """Find all CUDA device objects in ``obj``

    Search through ``obj`` and find all CUDA device objects, which are objects
    that either are known to ``dispatch`` or implement ``__cuda_array_interface__``.

    Parameters
    ----------
    obj: Any
        Object to search through

    Returns
    -------
    ret: Set[DeviceMemoryId]
        Set of CUDA device memory IDs
    """

def get_device_memory_objects_default(obj): ...
def get_device_memory_objects_python_sequence(seq): ...
def get_device_memory_objects_python_dict(seq): ...
def get_device_memory_objects_register_cupy(): ...
def get_device_memory_objects_register_cudf(): ...
def register_cupy(): ...
def register_pylibcudf(): ...
