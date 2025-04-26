from typing import Callable, Iterable, Iterator, Tuple, TypeVar, overload

class Info(object):
    """Information about a netCDF file.
    """
    @ overload
    def __init__(
        self, 
        filename: str
    ) -> None: ...
    
    @ overload
    def __str__(
        self
    ) -> str: ...
    
class Converter(object):
    """Create a new netCDF converted from a given netCDF file.
    """
    def __init__(
        self,
        old_filename: str, 
        new_filename: str,
    ) -> None: ...