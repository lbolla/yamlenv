__version__ = '0.3.1'


def load(stream):
    import yaml
    from . import env, loader

    data = yaml.load(stream, loader.Loader)
    return env.interpolate(data)
