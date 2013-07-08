#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tornado-geopy geocoding library.
# https://github.com/heynemann/tornado-geopy

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2013 Bernardo Heynemann heynemann@gmail.com

from setuptools import setup, find_packages
from tornado_geopy import __version__

tests_require = [
    'nose',
    'coverage',
    'yanc',
    'preggy==0.5.11',
    'mock',
    'tox',
    'ipdb',
    'coveralls',
]

setup(
    name='tornado-geopy',
    version=__version__,
    description='tornado-geopy is an asynchronous version of the awesome geopy library.',
    long_description='''
    tornado-geopy is an asynchronous version of the awesome geopy library.
    ''',
    keywords='geocoding locations google apis',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='http://github.com/heynemann/tornado-geopy/',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tornado>=3.1.0,<3.2.0',
        'geopy',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
