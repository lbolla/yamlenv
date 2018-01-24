# pylint: disable=undefined-variable
# flake8: noqa
from collections import Mapping, Set, Sequence
import os
import re

import yaml


__version__ = '0.2.0'


# dual python 2/3 compatability, inspired by the "six" library
string_types = (str, unicode) if str is bytes else (str, bytes)
iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()


def objwalk(obj, path=(), memo=None):
    if memo is None:
        memo = set()
    iterator = None
    if isinstance(obj, Mapping):
        iterator = iteritems
    elif isinstance(
            obj, (Sequence, Set)
    ) and not isinstance(obj, string_types):
        iterator = enumerate
    if iterator:
        if id(obj) not in memo:
            memo.add(id(obj))
            for path_component, value in iterator(obj):
                for result in objwalk(value, path + (path_component,), memo):
                    yield result
            memo.remove(id(obj))
    else:
        yield path, obj


class EnvVar(object):
    __slots__ = ['name', 'default']

    RE = re.compile(r'\$\{(?P<name>[^-]+)(?:-(?P<default>.+))?\}')

    def __init__(self, name, default):
        self.name = name
        self.default = default

    @property
    def value(self):
        value = os.environ.get(self.name)
        if value:
            return value
        if self.default:
            return self.default
        raise ValueError('Missing value and default for {}'.format(self.name))

    @classmethod
    def from_string(cls, s):
        if not isinstance(s, string_types):
            return None
        data = cls.RE.match(s)
        if not data:
            return None
        data = data.groupdict()
        return cls(data['name'], data['default'])


def interpolate_env(data):
    for path, obj in objwalk(data):
        e = EnvVar.from_string(obj)
        if e is not None:
            x = data
            for k in path[:-1]:
                x = x[k]
            x[path[-1]] = e.value
    return data


def load(stream):
    data = yaml.safe_load(stream)
    return interpolate_env(data)
