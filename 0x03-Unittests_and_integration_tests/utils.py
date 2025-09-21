#!/usr/bin/env python3
"""Generic utilities for github org client
"""
import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path.
    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value
    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b"])
    {"c": 1}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        try:
            nested_map = nested_map[key]
        except (KeyError, TypeError) as e:
            raise KeyError(key) from e
    return nested_map


def get_json(url: str) -> Dict:
    """Get JSON from remote URL.
    """
    r = requests.get(url)
    return r.json()


def memoize(fn: Callable) -> Callable:
    """Decorator to memoize a method.
    Example
    -------
    class MyClass:
        @memoize
        def a_method(self):
            print("a_method called")
            return 42
    >>> my_object = MyClass()
    >>> my_object.a_method
    a_method called
    42
    >>> my_object.a_method
    42
    """
    m = {}

    @wraps(fn)
    def memoized(self):
        """Memoized wraper fn.
        """
        if self not in m:
            m[self] = fn(self)
        return m[self]

    return property(memoized)