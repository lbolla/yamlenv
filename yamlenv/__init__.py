import yaml

from . import env, loader


__version__ = '0.3.2'


def load(stream):
    data = yaml.load(stream, loader.Loader)
    return env.interpolate(data)


def load_all(stream):
    for data in yaml.load_all(stream, loader.Loader):
        yield env.interpolate(data)
