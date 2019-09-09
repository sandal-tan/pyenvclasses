"""Dataclass wrapper to facilitate application configuration from the environment."""
# pylint: disable=all;

import os
from urllib import request
from distutils.core import setup
from setuptools import find_packages

INSTALL_REQUIRES = []
"""The dependencies required for this package."""

VERSION_FILE = 'VERSION'
"""The path to the version file."""

VERSION_SERVER = 'https://vxx.pairity.io'
"""The URL of the version server, which serves time-based versions in semver format."""

setup(
    name = 'py-envclasses',
    url = 'https://github.com/sandal-tan/py-envclasses',
    version=(open(VERSION_FILE).read() if os.path.exists(VERSION_FILE) else
             request.urlopen(VERSION_SERVER).read().decode()),
    description=__doc__,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Ian Baldwin',
    author_email='ianbldwn@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Documentation',
    ],
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    python_requires='~=3.7',
    package_data={'envclasses': ['VERSION']}
)
