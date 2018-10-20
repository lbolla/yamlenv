# pylint: disable=undefined-variable
import os
import re

try:
    from collections.abc import Mapping, Sequence, Set
except ImportError:
    # Python 2.7
    from collections import Mapping, Sequence, Set  # noqa

import six


def objwalk(obj, path=(), memo=None):
    if memo is None:
        memo = set()
    iterator = None
    if isinstance(obj, Mapping):
        iterator = six.iteritems
    elif isinstance(
            obj, (Sequence, Set)
    ) and not isinstance(obj, six.string_types):
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
    __slots__ = ['name', 'default', 'string']

    RE = re.compile(
        r'\$\{(?P<name>[^:-]+)(?:(?P<separator>:?-)(?P<default>.+))?\}')

    def __init__(self, name, default, string):
        self.name = name
        self.default = default
        self.string = string

    @property
    def value(self):
        value = os.environ.get(self.name)
        if value:
            return self.RE.sub(value, self.string)
        if self.default:
            return self.default
        raise ValueError('Missing value and default for {}'.format(self.name))

    @classmethod
    def from_string(cls, s):
        if not isinstance(s, six.string_types):
            return None
        data = cls.RE.search(s)
        if not data:
            return None
        data = data.groupdict()
        return cls(data['name'], data['default'], s)


def interpolate(data):
    for path, obj in objwalk(data):
        e = EnvVar.from_string(obj)
        if e is not None:
            x = data
            for k in path[:-1]:
                x = x[k]
            x[path[-1]] = e.value
    return data
