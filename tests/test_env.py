# pylint: disable=no-self-use
import os
import unittest

import yamlenv


class TestYamlEnv(unittest.TestCase):

    def test_load(self):
        self.assertEqual(yamlenv.load('''
a: 1
b: 2
        '''), {'a': 1, 'b': 2})

    def test_load_all(self):
        self.assertEqual(list(yamlenv.load_all('''
a: 1
b: 2
---
c: 3
        ''')), [{'a': 1, 'b': 2}, {'c': 3}])

    def test_fail_if_no_env(self):
        with self.assertRaises(ValueError):
            yamlenv.load('''
a: ${A}
b: 2
            ''')

    def test_interpolate_integer(self):
        os.environ['A'] = '1'
        self.assertEqual(yamlenv.load('''
a: ${A}
b: 2
            '''), {'a': '1', 'b': 2})

    def test_interpolate_string(self):
        os.environ['A'] = 'password'
        self.assertEqual(yamlenv.load('''
a: ${A}
b: 2
        '''), {'a': 'password', 'b': 2})

    def test_interpolate_within_characters(self):
        os.environ['A'] = 'def'
        self.assertEqual(yamlenv.load('''
a: abc${A}ghi
b: 2
        '''), {'a': 'abcdefghi', 'b': 2})

    def test_interpolate_string_alternative_separator(self):
        os.environ['A'] = 'password'
        self.assertEqual(yamlenv.load('''
a: ${A:-1}
b: 2
        '''), {'a': 'password', 'b': 2})

    def test_interpolate_string_prefer_env(self):
        os.environ['A'] = 'password'
        self.assertEqual(yamlenv.load('''
a: ${A-1}
b: 2
        '''), {'a': 'password', 'b': 2})

    def test_interpolate_default(self):
        self.assertEqual(yamlenv.load('''
a: ${A-1}
b: 2
            '''), {'a': '1', 'b': 2})

    def test_interpolate_default_alternative_separator(self):
        self.assertEqual(yamlenv.load('''
a: ${A:-1}
b: 2
            '''), {'a': '1', 'b': 2})

    def test_interpolate_nested(self):
        self.assertEqual(yamlenv.load('''
a: 1
b:
  b1: 21
  b2: ${B-22}
            '''), {'a': 1, 'b': {'b1': 21, 'b2': '22'}})
