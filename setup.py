from setuptools import setup, find_packages

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='yamlenv',
    version='0.6.0',
    author="Lorenzo Bolla",
    author_email="lbolla@gmail.com",
    description="Interpolate Yaml files with env vars",
    long_description=long_description,
    url="https://github.com/lbolla/yamlenv",
    packages=find_packages('.'),
    install_requires=[
        'PyYAML>=3.12',
        'six>=1.10',
        'typing; python_version<"3.6"',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
