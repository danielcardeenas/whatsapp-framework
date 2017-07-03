#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import platform
import sys

# Main dependences
# Custom dependences
deps = ['requests', 'pytube', 'moviepy', 'wolframalpha', 'prettytable', 'trueskill', 'deuces']

if sys.version_info < (2,7):
    deps += ['importlib']

if platform.system().lower() == "windows":
    deps.append('pyreadline')
else:
    try:
        import readline
    except ImportError:
        deps.append('readline')

setup(
    name='mac bot',
    version=1,
    url='http://github.com/danielcardeenas/whatsapp-framework',
    license='GPL-3+',
    author='Daniel Cardenas',
    tests_require=[],
    install_requires = deps,
    #cmdclass={'test': PyTest},
    author_email='danielcardeenas@gmail.com',
    description='A WhatsApp bot',
    #long_description=long_description,
    packages= find_packages(),
    include_package_data=True,
    platforms='any',
    #test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Alpha',
        'Natural Language :: English - Spanish',
        #'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    #extras_require={
    #    'testing': ['pytest'],
    #}
)
