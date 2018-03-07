from setuptools import setup, find_packages

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='yamlenv',
    version='0.4.0',
    author="Lorenzo Bolla",
    author_email="lbolla@gmail.com",
    description="Interpolate Yaml files with env vars",
    long_description=long_description,
    url="https://github.com/lbolla/yamlenv",
    packages=find_packages('.'),
    install_requires=[
        'PyYAML>=3.12',
        'six>=1.10',
    ],
)
