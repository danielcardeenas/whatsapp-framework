#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pykemon.models

This files holds all the class definitions representing resources from PokeAPI.
"""


def buildr(bundle, key):
    " Builds a dict of NAME:URI for each item in the bundle "
    return {f['name']: f['resource_uri'] for f in bundle[key]}


class DateTimeObject(object):

    def __init__(self, bundle):
        self.name = bundle['name']
        self.resource_uri = bundle['resource_uri']
        self.created = bundle['created']
        self.modified = bundle['modified']


class Pokemon(DateTimeObject):
    """
    This class represents a single Pokemon resource
    """

    def __init__(self, bundle):
        super(Pokemon, self).__init__(bundle)
        self.id = bundle['national_id']
        self.abilities = buildr(bundle, 'abilities')
        self.egg_groups = buildr(bundle, 'egg_groups')
        self.evolutions = {
            f['to']: f['resource_uri'] for f in bundle['evolutions']}
        self.descriptions = buildr(bundle, 'descriptions')
        self.moves = buildr(bundle, 'moves')
        self.types = buildr(bundle, 'types')
        self.catch_rate = bundle['catch_rate']
        self.species = bundle['species']
        self.hp = bundle['hp']
        self.attack = bundle['attack']
        self.defense = bundle['defense']
        self.sp_atk = bundle['sp_atk']
        self.sp_def = bundle['sp_def']
        self.speed = bundle['speed']
        self.total = bundle['total']
        self.egg_cycles = bundle['egg_cycles']
        self.ev_yield = bundle['ev_yield']
        self.exp = bundle['exp']
        self.growth_rate = bundle['growth_rate']
        self.height = bundle['height']
        self.weight = bundle['weight']
        self.happiness = bundle['happiness']
        self.male_female_ratio = bundle['male_female_ratio']
        self.sprites = buildr(bundle, 'sprites')

    def __repr__(self):
        return '<Pokemon - %s>' % self.name.capitalize()


class Move(DateTimeObject):
    """
    This class represents a single Move resource
    """

    def __init__(self, bundle):
        super(Move, self).__init__(bundle)
        self.id = bundle['id']
        self.accuracy = bundle['accuracy']
        self.category = bundle['category']
        self.power = bundle['power']
        self.pp = bundle['pp']

    def __repr__(self):
        return '<Move - %s>' % self.name.capitalize()


class Type(DateTimeObject):
    """
    This class represents a single Type Resource
    """

    def __init__(self, bundle):
        super(Type, self).__init__(bundle)
        self.id = bundle['id']
        self.name = bundle['name']
        self.ineffective = buildr(bundle, 'ineffective')
        self.resistance = buildr(bundle, 'resistance')
        self.super_effective = buildr(bundle, 'super_effective')
        self.weakness = buildr(bundle, 'weakness')

    def __repr__(self):
        return '<Type - %s>' % self.name.capitalize()


class Ability(DateTimeObject):
    """
    This class represents a single Ability resource
    """

    def __init__(self, bundle):
        super(Ability, self).__init__(bundle)
        self.id = bundle['id']
        self.description = bundle['description']

    def __repr__(self):
        return '<Ability - %s>' % self.name.capitalize()


class Egg(DateTimeObject):
    """
    This class represents a single Egg group resource
    """

    def __init__(self, bundle):
        super(Egg, self).__init__(bundle)
        self.id = bundle['id']
        self.pokemon = buildr(bundle, 'pokemon')

    def __repr__(self):
        return '<Egg - %s>' % self.name.capitalize()


class Description(DateTimeObject):
    """
    This class represents a single Description resource
    """

    def __init__(self, bundle):
        super(Description, self).__init__(bundle)
        self.id = bundle['id']
        self.description = bundle['description']
        self.pokemon = bundle['pokemon']
        self.games = buildr(bundle, 'games')

    def __repr__(self):
        return '<Description - %s>' % self.name.capitalize()


class Sprite(DateTimeObject):
    """
    This class represents a single Sprite resource
    """

    def __init__(self, bundle):
        super(Sprite, self).__init__(bundle)
        self.id = bundle['id']
        self.pokemon = bundle['pokemon']
        self.image = bundle['image']

    def __repr__(self):
        return '<Sprite - %s>' % self.name.capitalize()


class Game(DateTimeObject):
    """
    This class represents a single Game resource
    """

    def __init__(self, bundle):
        super(Game, self).__init__(bundle)
        self.id = bundle['id']
        self.generation = bundle['generation']
        self.release_year = bundle['release_year']

    def __repr__(self):
        return '<Game - %s>' % self.name.capitalize()
