#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from code.entity import Entity


class Enemy(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.direction = 1
        self.start_x = position[0]

        # inimigo normal
        if name == 'monstro':
            self.life = 3
            self.speed = 2

            # hitbox do inimigo
            self.rect = pygame.Rect(position[0] + 45, position[1] + 20, 35, 35)

        # boss
        elif name == 'boss':
            self.life = 10
            self.speed = 1

            # hitbox do boss
            self.rect = pygame.Rect(position[0] + 20, position[1] + 20, 120, 180)

    def move(self):

        # monstro normal
        if self.name == 'monstro':
            self.rect.x += self.speed * self.direction

            # limite da patrulha
            if self.rect.x > self.start_x + 100:
                self.direction = -1

            if self.rect.x < self.start_x - 100:
                self.direction = 1

        # boss
        elif self.name == 'boss':
            pass