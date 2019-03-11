import typing as T
import yaml

from yamlenv import env, loader
from yamlenv.types import Stream


__version__ = '0.7.0'


def load(stream):
    # type: (Stream) -> T.Any
    data = yaml.load(stream, loader.Loader)
    return env.interpolate(data)


def load_all(stream):
    # type: (Stream) -> T.Iterator[T.Any]
    for data in yaml.load_all(stream, loader.Loader):
        yield env.interpolate(data)
