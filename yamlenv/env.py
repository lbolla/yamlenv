import os
import re
import yaml

try:
    from collections.abc import Mapping, Sequence, Set
except ImportError:
    # Python 2.7
    from collections import Mapping, Sequence, Set  # noqa

import six
import typing as T

from yamlenv.types import Cache, Obj, ObjIFunc, Path, WalkType


def objwalk(obj, path=None, memo=None):
    # type: (Obj, T.Optional[Path], T.Optional[Cache]) -> WalkType
    if path is None:
        path = tuple()
    if memo is None:
        memo = set()
    iterator = None  # type: T.Optional[ObjIFunc]
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
    '''Follow Bash expansion rules.
    https://www.gnu.org/software/bash/manual/html_node\
/Shell-Parameter-Expansion.html
    '''
    __slots__ = ['name', 'separator', 'default', 'string']

    RE = re.compile(
        r'\$\{(?P<name>[^:-]+)((?P<separator>:?)-(?P<default>.*))?\}')

    def __init__(self, name, separator, default, string):
        # type: (str, str, str, str) -> None
        self.name = name
        self.separator = separator
        self.default = default
        self.string = string

    @property
    def allow_null_default(self):
        # type: () -> bool
        return self.separator == ''

    @property
    def value(self):
        # type: () -> str
        value = os.environ.get(self.name)
        if value:
            return self.RE.sub(value, self.string)
        if self.allow_null_default or self.default:
            return self.RE.sub(self.default, self.string)
        raise ValueError('Missing value and default for {}'.format(self.name))

    @property
    def yaml_value(self):
        # type: () -> T.Any
        return yaml.safe_load(self.value)

    @classmethod
    def from_string(cls, s):
        # type: (str) -> T.Optional[EnvVar]
        if not isinstance(s, six.string_types):
            return None
        data = cls.RE.search(s)
        if not data:
            return None
        gd = data.groupdict()
        return cls(gd['name'], gd['separator'], gd['default'], s)


def interpolate(data):
    # type: (T.Any) -> Obj
    for path, obj in objwalk(data):
        e = EnvVar.from_string(obj)
        if e is not None:
            x = data
            for k in path[:-1]:
                x = x[k]
            x[path[-1]] = e.yaml_value
    return data
