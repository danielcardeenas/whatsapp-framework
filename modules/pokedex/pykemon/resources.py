# -*- coding: utf-8 -*-

from beckett.resources import BaseResource


class PokemonResource(BaseResource):
    class Meta(BaseResource.Meta):
        name = 'Pokemon'
        resource_name = 'pokemon'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'national_id',
            'abilities',
            'egg_groups',
            'evolutions',
            'descriptions',
            'moves',
            'types',
            'catch_rate',
            'species',
            'hp',
            'attack',
            'defense',
            'name',
            'sp_atk',
            'sp_def',
            'speed',
            'total',
            'egg_cycles',
            'ev_yield',
            'exp',
            'growth_rate',
            'height',
            'weight',
            'happiness',
            'male_female_ratio',
            'sprites',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)


class MoveResource(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Move'
        resource_name = 'move'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'id',
            'accuracy',
            'category',
            'power',
            'pp',
            'name',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)


class TypeResource(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Type'
        resource_name = 'type'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'id',
            'name',
            'ineffective',
            'resistance',
            'super_effective',
            'weakness',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)


class AbilityResource(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Ability'
        resource_name = 'ability'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'id',
            'name',
            'description',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)


class EggResource(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Egg'
        resource_name = 'egg'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'id',
            'name',
            'pokemon',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)


class DescriptionResource(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Description'
        resource_name = 'description'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'id',
            'name',
            'description',
            'pokemon',
            'games',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)


class SpriteResource(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Sprite'
        resource_name = 'sprite'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'id',
            'name',
            'pokemon',
            'image',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)


class GameResource(BaseResource):

    class Meta(BaseResource.Meta):
        name = 'Game'
        resource_name = 'game'
        identifier = 'id'
        methods = (
            'get',
        )
        attributes = (
            'created',
            'modified',
            'id',
            'name',
            'generation',
            'release_year',
        )

    @staticmethod
    def get_single_resource_url(url, uid, **kwargs):
        # Needs a slash on the end!
        return '{}/{}/'.format(url, uid)
