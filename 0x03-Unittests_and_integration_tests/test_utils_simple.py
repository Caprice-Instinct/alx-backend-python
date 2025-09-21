#!/usr/bin/env python3
"""Test utils module
"""
import unittest
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map function
    """

    def test_access_nested_map_case_1(self):
        """Test access_nested_map with nested_map={'a': 1}, path=('a',)"""
        self.assertEqual(access_nested_map({"a": 1}, ("a",)), 1)

    def test_access_nested_map_case_2(self):
        """Test access_nested_map with nested_map={'a': {'b': 2}}, path=('a',)"""
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a",)), {"b": 2})

    def test_access_nested_map_case_3(self):
        """Test access_nested_map with nested_map={'a': {'b': 2}}, path=('a', 'b')"""
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a", "b")), 2)