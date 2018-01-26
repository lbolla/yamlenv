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
