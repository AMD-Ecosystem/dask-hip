from _typeshed import Incomplete

is_spillable_object: Incomplete

def _(seq): ...
def register_cudf(): ...
def cudf_spilling_status() -> bool | None:
    """Check the status of cudf's built-in spilling

    Returns:
        - True if cudf's internal spilling is enabled, or
        - False if it is disabled, or
        - None if the current version of cudf doesn't support spilling, or
        - None if cudf isn't available.
    """
