#!/usr/bin/python
# -*- coding: utf-8 -*-


from code.enemy import Enemy
from code.player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):

        match entity_name:

            case 'Player1':
                return Player('Player1', position)

            case 'Monster':
                return Enemy('monstro', position)

            case 'Boss':
                return Enemy('boss', position)
