#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Paul Hallett'
__email__ = 'hello@phalt.co'
__version__ = '0.2.0'
__copyright__ = 'Copyright Paul Hallett 2016'
__license__ = 'BSD'

from .api import get, V1Client  # NOQA
from .exceptions import ResourceNotFoundError  # NOQA


"""

========
Pykemon
========

A Python wrapper for PokeAPI (http://pokeapi.co)

Usage:

>>> import pykemon
>>> pykemon.get(pokemon='bulbasaur')
<Pokemon - Bulbasaur>
>>> pykemon.get(pokemon_id=151)
<Pokemon - Mew>

"""
