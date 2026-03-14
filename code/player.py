#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)



        self.frames = []

        for i in range(1, 8):
            frame = pygame.image.load(f"assets/Player{i}.png").convert_alpha()
            self.frames.append(frame)

        self.run_frames = []

        for i in range(1, 9):
            frame = pygame.image.load(f"assets/Player_run{i}.png").convert_alpha()
            self.run_frames.append(frame)

        self.attack_frames = []

        for i in range(1, 5):
            frame = pygame.image.load(f"assets/Player_attack{i}.png").convert_alpha()
            self.attack_frames.append(frame)



        self.frame_index = 0
        self.animation_speed = 0.15
        self.surf = self.frames[self.frame_index]
        self.rect = self.surf.get_rect(left=position[0], top=position[1])


        self.state = "idle"
        self.facing_right = True
        self.attacking = False

        self.spawn_magic = False
        self.attack_shot_done = False

        self.speed = 4
        self.gravity = 0
        self.jump_speed = -13
        self.on_ground = False
        self.life = 3
        self.invulnerable = False
        self.invulnerable_time = 0

          # animaçao parado
    def animate_idle(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        x = self.rect.x
        bottom = self.rect.bottom

        self.surf = self.frames[int(self.frame_index)]

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self.rect = self.surf.get_rect(left=x, bottom=bottom)


       # animaçao correr
    def animate_run(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.run_frames):
            self.frame_index = 0

        x = self.rect.x
        bottom = self.rect.bottom

        self.surf = self.run_frames[int(self.frame_index)]

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self.rect = self.surf.get_rect(left=x, bottom=bottom)

         # animaçao atacar
    def animate_attack(self):
        self.frame_index += self.animation_speed

        if int(self.frame_index) == 2 and not self.attack_shot_done:
            self.spawn_magic = True
            self.attack_shot_done = True

        if self.frame_index >= len(self.attack_frames):
            self.frame_index = 0
            self.attacking = False
            self.state = "idle"
            self.attack_shot_done = False

        x = self.rect.x
        bottom = self.rect.bottom

        self.surf = self.attack_frames[int(self.frame_index)]

        if not self.facing_right:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self.rect = self.surf.get_rect(left=x, bottom=bottom)


    def move(self):
        pressed_key = pygame.key.get_pressed()
        moving = False

        if pressed_key[pygame.K_c] and not self.attacking:
            self.attacking = True
            self.state = "attack"
            self.frame_index = 0

          # travar ataque
        if self.attacking:
            self.animate_attack()

            if self.rect.left < 0:
                self.rect.left = 0

            return


        if pressed_key[pygame.K_d]:
            self.rect.x += self.speed
            moving =  True
            self.facing_right = True

        if pressed_key[pygame.K_a]:
            self.rect.x -= self.speed
            moving = True
            self.facing_right = False

        if self.rect.left < 0:
            self.rect.left = 0

        if moving:
            if self.state != "run":
                self.frame_index = 0
                self.state = "run"
            self.animate_run()
        else:
            if self.state != "idle":
                self.frame_index = 0
                self.state = "idle"
            self.animate_idle()

        # empede que o player sai  da tela
        if self.rect.left < 0:
            self.rect.left = 0

    def apply_gravity(self):
        self.gravity += 0.8
        self.rect.y += self.gravity

    def jump(self):
        if self.on_ground:
            self.gravity = self.jump_speed
            self.on_ground = False
