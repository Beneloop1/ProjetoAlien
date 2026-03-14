#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class Magic:
    def __init__(self, x, y, facing_right):
        self.frames = []

        for i in range(1, 9):
            frame = pygame.image.load(f"assets/Player_skill{i}.png").convert_alpha()
            self.frames.append(frame)

        self.frame_index = 0
        self.animation_speed = 0.20
        self.surf = self.frames[self.frame_index]

        # hitbox fixa da magia
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)


        self.speed = 7
        self.facing_right = facing_right
        self.alive = True

    def update(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        center = self.rect.center
        self.surf = self.frames[int(self.frame_index)]

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)


        if self.facing_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed