__version__ = '0.2.0'


def load(stream):
    import yaml
    from . import env, loader

    data = yaml.load(stream, loader.Loader)
    return env.interpolate(data)
