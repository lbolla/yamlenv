import os
import json
import typing as T

import six
import yaml


class LoaderMeta(type):

    def __new__(mcs, __name__, __bases__, __dict__):  # type: ignore
        """Add include constructer to class."""

        # register the include constructor on the class
        cls = mcs.__class__.__new__(mcs, __name__, __bases__, __dict__)
        cls.add_constructor('!include', cls.construct_include)

        return cls


@six.add_metaclass(LoaderMeta)
class Loader(yaml.Loader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream, filenames_seen=None):
        # type: (T.IO[str], T.Optional[T.Set[str]]) -> None
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        self._filenames_seen = filenames_seen or set()
        yaml.Loader.__init__(self, stream)

    def _remeber(self):
        # type: () -> T.Callable[[T.IO[str]], Loader]
        """Create a loader with the same filenames cache."""
        def loader(stream):
            # type: (T.IO[str]) -> Loader
            return Loader(stream, self._filenames_seen)
        return loader

    def construct_include(self, node):
        # type: (T.Any) -> T.Any
        """Include file referenced at node."""

        filename = os.path.abspath(
            os.path.join(
                self._root, self.construct_scalar(node)))  # type: ignore
        extension = os.path.splitext(filename)[1].lstrip('.')

        if filename in self._filenames_seen:
            raise ValueError('Circular !include {}'.format(filename))
        self._filenames_seen.add(filename)

        with open(filename, 'r') as f:
            if extension in ('yaml', 'yml'):
                return yaml.load(f, self._remeber())
            if extension == 'json':
                return json.load(f)
            return f.read()
