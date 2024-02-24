from ctypes import (
    cdll,
    CDLL,
    POINTER,
    c_uint,
    c_uint8,
    c_uint16,
    c_uint64,
)
from importlib.machinery import EXTENSION_SUFFIXES
from os import stat

c_uint_p = POINTER(c_uint)
c_uint8_p = POINTER(c_uint8)
c_uint16_p = POINTER(c_uint16)
c_uint64_p = POINTER(c_uint64)


def auto_import(lib_name: str) -> CDLL:
    """Import C shared object/DLL
    without specifying extension.
    (! UNTESTED)

    Args:
        lib_name (str): Library name, without extensions


        - Wrong::

            auto_import('clib.so')
            auto_import('clib.cpython-311-x86_64-linux-gnu.so')

        - Right::

            auto_import('clib')

    Raises:
        ImportError: Raise error if file not found.

    Returns:
        CDLL: Loaded DLL object
    """

    _so_file = ''
    for suffix in EXTENSION_SUFFIXES:
        file = f'{lib_name}{suffix}'
        try:
            stat(file)
            _so_file = file
            break
        except FileNotFoundError:
            continue
    else:
        raise ImportError(f'Can find {lib_name} library.'
                          + f'Should be any of: {", ".join([ f"`{lib_name}{s}`" for s in EXTENSION_SUFFIXES])}.'  # noqa: E501
                          + 'Make sure it exist, or in the correct path')

    return cdll.LoadLibrary(_so_file)
