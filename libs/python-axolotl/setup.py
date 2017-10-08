# -*- coding: utf-8 -*-

import sys

import axolotl
from setuptools import find_packages, setup

deps = ['pycrypto', 'python-axolotl-curve25519', 'protobuf>=3.0.0.b2']

setup(
    name='python-axolotl',
    version=axolotl.__version__ ,
    packages= find_packages(),
    install_requires = deps,
    license='GPLv3 License',
    author='Tarek Galal',
    author_email='tare2.galal@gmail.com',
    description="Python port of libaxolotl-android, originally written by Moxie Marlinspik",
    url='https://github.com/tgalal/python-axolotl',
    download_url='https://github.com/tgalal/python-axolotl/releases',
    platforms='any',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Security :: Cryptography',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
