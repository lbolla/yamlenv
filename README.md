# Yamlenv

Interpolate YaML files with environmental variables.

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

More examples are available in the tests.
