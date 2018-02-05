# pylint: disable=no-self-use
import tempfile
import unittest

import yamlenv


class TestYamlInclude(unittest.TestCase):

    def test_non_existing(self):
        with self.assertRaises(IOError):
            yamlenv.load('''
    a: 1
    b: !include non-existing.yaml
            ''')

    def test_empty_file(self):
        f = tempfile.NamedTemporaryFile(suffix='.yaml')

        data = yamlenv.load('''
a: 1
b: !include {}
        '''.format(f.name))

        self.assertEqual(data, {'a': 1, 'b': None})

    def test_include(self):
        f = tempfile.NamedTemporaryFile(suffix='.yaml')
        f.write(b'2')
        f.flush()

        data = yamlenv.load('''
a: 1
b: !include {}
        '''.format(f.name))

        self.assertEqual(data, {'a': 1, 'b': 2})

    def test_circular_self(self):
        f = tempfile.NamedTemporaryFile(suffix='.yaml')

        f.write('''
a: !include {}
        '''.format(f.name).encode())
        f.flush()
        f.seek(0)

        with self.assertRaises(ValueError):
            yamlenv.load(f)

    def test_circular(self):
        f1 = tempfile.NamedTemporaryFile(suffix='.yaml')
        f2 = tempfile.NamedTemporaryFile(suffix='.yaml')

        f1.write('''
a: !include {}
        '''.format(f2.name).encode())
        f1.flush()
        f1.seek(0)

        f2.write('''
a: !include {}
        '''.format(f1.name).encode())
        f2.flush()
        f2.seek(0)

        with self.assertRaises(ValueError):
            yamlenv.load(f1)
