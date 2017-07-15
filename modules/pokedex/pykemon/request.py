#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pykemon.request

This is the request factory for pykemon
All API calls made to the PokeAPI website go from here.
"""

BASE_URI = 'http://pokeapi.co/api/v1'

CHOICES = ['pokedex', 'pokedex_id', 'pokemon', 'pokemon_id', 'move', 'move_id',
           'ability', 'ability_id', 'type', 'type_id', 'egg',
           'egg_id', 'description', 'description_id', 'sprite',
           'sprite_id', 'game', 'game_id']

import requests
import simplejson
from simplejson import JSONDecodeError
from .models import Pokemon, Move, Type, Ability, Egg, Description, Sprite, Game
from .exceptions import ResourceNotFoundError

CLASSES = {
    'pokemon': Pokemon,
    'move': Move,
    'type': Type,
    'ability': Ability,
    'egg': Egg,
    'description': Description,
    'sprite': Sprite,
    'game': Game
}


def _request(uri):
    """
    Just a wrapper around the request.get() function
    """

    r = requests.get(uri)

    if r.status_code == 200:
        return _to_json(r.text)
    else:
        raise ResourceNotFoundError(
            'API responded with %s error' % str(r.status_code))


def _to_json(data):
    try:
        content = simplejson.loads(data)
        return content
    except JSONDecodeError:
        raise JSONDecodeError('Error decoding data', data, 0)


def _compose(choice):
    """
    Figure out exactly what resource we're requesting and return the correct
    class.
    """
    nchoice = list(choice.keys())[0]
    id = list(choice.values())[0]

    if '_id' in nchoice:
        nchoice = nchoice[:-3]
    return ('/'.join([BASE_URI, nchoice, str(id), '']), nchoice)


def make_request(choice):
    """
    The entry point from pykemon.api.
    Call _request and _compose to figure out the resource / class
    and return the correct constructed object
    """
    uri, nchoice = _compose(choice)
    data = _request(uri)

    resource = CLASSES[nchoice]
    return resource(data)
