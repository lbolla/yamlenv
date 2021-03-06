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
            '''), {'a': 1, 'b': 2})

    def test_interpolate_string(self):
        os.environ['A'] = 'password'
        self.assertEqual(yamlenv.load('''
a: ${A}
b: 2
        '''), {'a': 'password', 'b': 2})

    def test_interpolate_two_values(self):
        os.environ['A'] = '1'
        os.environ['B'] = 'foo'
        self.assertEqual(yamlenv.load('''
a: ${A} ${B}
            '''), {'a': "1 foo"})

    def test_interpolate_two_values_with_defaults(self):
        self.assertEqual(yamlenv.load('''
a: ${C:-foo} ${D:-bar}
            '''), {'a': "foo bar"})

    def test_interpolate_invalid_yaml_value(self):
        self.assertEqual(yamlenv.load('''
{'a': {'b': '{foo} ${C:-foo}'}}
            '''), {'a': {'b': "{foo} foo"}})

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
            '''), {'a': 1, 'b': 2})

    def test_interpolate_default_alternative_separator(self):
        self.assertEqual(yamlenv.load('''
a: ${A:-1}
b: 2
            '''), {'a': 1, 'b': 2})

    def test_interpolate_nested(self):
        self.assertEqual(yamlenv.load('''
a: 1
b:
  b1: 21
  b2: ${B-22}
            '''), {'a': 1, 'b': {'b1': 21, 'b2': 22}})

    def test_interpolate_embedded(self):
        self.assertEqual(yamlenv.load('''
a: ${FOO:-foo} bar
'''), {'a': 'foo bar'})

    def test_interpolate_embedded_integer(self):
        self.assertEqual(yamlenv.load('''
a: ${FOO:-7} bar
'''), {'a': '7 bar'})


    def test_interpolate_default_empty(self):
        self.assertEqual(yamlenv.load('''
a: bar ${FOO-} bar
'''), {'a': 'bar  bar'})

    def test_default_empty(self):
        self.assertEqual(yamlenv.load('''
a: ${FOO-}
'''), {'a': None})

    def test_default_does_not_exist(self):
        with self.assertRaises(ValueError):
            yamlenv.load('''
a: ${FOO:-} bar
''')
