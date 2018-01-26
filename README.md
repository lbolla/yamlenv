# Yamlenv

[![Build Status](https://travis-ci.org/lbolla/yamlenv.svg?branch=master)](https://travis-ci.org/lbolla/yamlenv)

Interpolate YaML files with environmental variables and other YaML files.

Given a YaML string like:

    a: ${A}
    b: 2

and an environmental variable `$A` with value `hello`, `yamlenv.load`
would return:

    {
        a: 'hello',
        b: 2
    }

Default values are supported:

    yamlenv.load('''
        a: ${A, 'hello'}
        b: 2
    ''') == {
        'a': 'hello',
        'b': 2
    }

YaML files can include other YaML files, too. E.g. if `b.yaml`
contains "2", then:

    yamlenv.load('''
        a: 1
        b: !include b.yaml
    ''') == {
        'a': 1
        'b': 2
    }

The included YaML file can be as complex as necessary.

More examples are available in the tests.
