import os
import re
import yaml
import yaml.parser

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
        r'\$\{(?P<name>[^:-]+?)((?P<separator>:?)-(?P<default>.*?))?\}')

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
            return self.RE.sub(value, self.string, count=1)
        if self.allow_null_default or self.default:
            return self.RE.sub(self.default, self.string, count=1)
        raise ValueError('Missing value and default for {}'.format(self.name))

    @property
    def maybe_yaml_value(self):
        # type: () -> T.Any
        v = self.value
        try:
            return yaml.safe_load(v)
        except yaml.parser.ParserError:
            return v

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
    while True:
        more = False
        for path, obj in objwalk(data):
            e = EnvVar.from_string(obj)
            if e is not None:
                more = True
                x = data
                for k in path[:-1]:
                    x = x[k]
                x[path[-1]] = e.maybe_yaml_value
        if not more:
            break
    return data
