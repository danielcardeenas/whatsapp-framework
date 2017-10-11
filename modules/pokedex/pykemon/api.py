#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pykemon.api

User interaction with this package is done through this file.
"""

from beckett.clients import BaseClient

from .request import CHOICES
from .request import make_request

from .resources import (
    MoveResource, PokemonResource, TypeResource, AbilityResource, EggResource,
    DescriptionResource, SpriteResource, GameResource
)


def get(**kwargs):
    """
    Make a request to the PokeAPI server and return the requested resource

    Resource choices:

    pokedex_id
    pokemon
    pokemon_id
    move_id
    ability_id
    type_id
    egg_id
    description_id
    sprite_id
    game_id

    """
    if len(list(kwargs.keys())) > 1:
        raise ValueError('Too many arguments. Only pass 1 argument')

    if list(kwargs.keys())[0] in CHOICES:
        return make_request(kwargs)

    else:
        raise ValueError('An invalid argument was passed')


'''
Modified to v2 api
'''
class V1Client(BaseClient):

    class Meta(BaseClient.Meta):
        name = 'pykemon-v1-client'
        base_url = 'http://pokeapi.co/api/v2'
        resources = (
            MoveResource,
            PokemonResource,
            TypeResource,
            AbilityResource,
            EggResource,
            DescriptionResource,
            SpriteResource,
            GameResource,
        )
