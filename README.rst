Yamlenv
=======

|Build Status| |PyPi package|

Interpolate YaML files with environmental variables and other YaML
files.

Given a YaML string like:

.. code-block:: yaml

    a: ${A}
    b: 2

and an environmental variable ``$A`` with value ``hello``,
``yamlenv.load`` would return:

.. code-block:: python

    {
        a: 'hello',
        b: 2
    }

Including YAML literals as environment variables is also
supported - so if the environment variable ``$A`` was set to
``false``, ``yamlenv.load`` would return:

.. code-block:: python

    {
        a: False,
        b: 2
    }


Default values are supported:

.. code-block:: python

    yamlenv.load('''
        a: ${A:-hello}
        b: 2
    ''') == {
        'a': 'hello',
        'b': 2
    }

As in Bash, defaulting can be done with either `:-` (to not allow empty
defaults) or with `-` to allow empty values.

The environmental variable can be embedded in a larger string, too:

.. code-block:: python

    yamlenv.load('''
        a: foo ${A:-bar} baz
        b: 2
    ''') == {
        'a': 'foo bar baz',
        'b': 2
    }

YaML files can include other YaML files, too. E.g. if ``b.yaml``
contains "2", then:

.. code-block:: python

    yamlenv.load('''
        a: 1
        b: !include b.yaml
    ''') == {
        'a': 1
        'b': 2
    }

The included YaML file can be as complex as necessary.

More examples are available in the tests.

.. |Build Status| image:: https://travis-ci.org/lbolla/yamlenv.svg?branch=master
   :target: https://travis-ci.org/lbolla/yamlenv

.. |PyPi package| image:: https://badge.fury.io/py/yamlenv.svg
    :target: https://badge.fury.io/py/yamlenv
