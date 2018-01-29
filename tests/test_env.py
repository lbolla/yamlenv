# pylint: disable=no-self-use
import os
import unittest

import yamlenv


class TestYamlEnv(unittest.TestCase):

    def test_load(self):
        assert yamlenv.load('''
a: 1
b: 2
        ''') == {'a': 1, 'b': 2}

    def test_load_all(self):
        assert list(yamlenv.load_all('''
a: 1
b: 2
---
c: 3
        ''')) == [{'a': 1, 'b': 2}, {'c': 3}]

    def test_fail_if_no_env(self):
        with self.assertRaises(ValueError):
            yamlenv.load('''
a: ${A}
b: 2
            ''')

    def test_interpolate_integer(self):
        os.environ['A'] = '1'
        assert yamlenv.load('''
a: ${A}
b: 2
            ''') == {'a': '1', 'b': 2}

    def test_interpolate_string(self):
        os.environ['A'] = 'password'
        assert yamlenv.load('''
a: ${A}
b: 2
        ''') == {'a': 'password', 'b': 2}

    def test_interpolate_default(self):
        assert yamlenv.load('''
a: ${A-1}
b: 2
            ''') == {'a': '1', 'b': 2}

    def test_interpolate_nested(self):
        assert yamlenv.load('''
a: 1
b:
  b1: 21
  b2: ${B-22}
            ''') == {'a': 1, 'b': {'b1': 21, 'b2': '22'}}
