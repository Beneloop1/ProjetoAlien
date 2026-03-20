#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from code.magic import Magic
from code.Const import WIN_WIDTH
from code.entity import Entity
from code.entityFactory import EntityFactory
import random


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.magic_list = []

        self.map_width = 2300
        self.max_scroll = self.map_width - WIN_WIDTH

        self.finished = False
        self.boss_arena = False
        self.boss = None
        self.boss_spawned = False
        self.boss_attack_timer = 0
        self.boss_magic_list = []
        self.arena_scroll = 0
        self.boss_shots = 0
        self.boss_shot_delay = 0


        # plataformas
        self.platforms = [
            # chão
            pygame.Rect(0, 300, self.map_width, 50),
            pygame.Rect(200, 210, 100, 20),
            pygame.Rect(300, 160, 100, 20),
            pygame.Rect(600, 210, 200, 20),
            pygame.Rect(780, 160, 70, 20),
            pygame.Rect(880, 210, 130, 20),
            pygame.Rect(960, 120, 100, 20),
            pygame.Rect(1100, 210, 80, 20),

            #pygame.Rect(1100, 210, 130, 20),
           # pygame.Rect(1050, 130, 90, 20),

            # escada subindo
            pygame.Rect(1340, 240, 80, 20),
            pygame.Rect(1400, 200, 80, 20),
            pygame.Rect(1460, 160, 80, 20),
            pygame.Rect(1520, 120, 80, 20),

            # topo
            pygame.Rect(1580, 80, 250, 20),

            pygame.Rect(1570, 80, 80, 20),
            pygame.Rect(1680, 210, 80, 20),


        ]

        self.walls = [
            pygame.Rect(1330, 240, 10, 60),  # entrada da escada
            pygame.Rect(1410, 200, 10, 40),  # fim do 1º degrau
            pygame.Rect(1470, 160, 10, 40),  # fim do 2º degrau
            pygame.Rect(1530, 120, 10, 40),  # fim do 3º degrau
            pygame.Rect(1590, 80, 10, 40),  # fim do 4º degrau
        ]


        self.player = EntityFactory.get_entity('Player1', (10, 200))

        # camadas do fundo
        self.bg0 = pygame.image.load('./assets/Level1Bg0.png').convert_alpha()
        self.bg1 = pygame.image.load('./assets/Level1Bg1.png').convert_alpha()
        self.bg2 = pygame.image.load('./assets/Level1Bg2.png').convert_alpha()
        self.bg3 = pygame.image.load('./assets/Level1Bg3.png').convert_alpha()


        # plataforma
        self.platform_img = pygame.image.load("./assets/Level1BgPlaforma.png").convert_alpha()

        # monstro
        self.enemy = EntityFactory.get_entity('Monster', (600, 220))
        self.enemy2 = EntityFactory.get_entity('Monster', (1180, 220))

        self.scroll = 0
        self.ground_y = 300

    def show_end_screen(self, message):
        font_title = pygame.font.SysFont("Arial", 48, bold=True)
        font_text = pygame.font.SysFont("Arial", 28)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    return

            overlay = pygame.Surface((WIN_WIDTH, 350))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))

            self.window.blit(overlay, (0, 0))

            title = font_title.render(message, True, (255, 255, 255))
            text = font_text.render("Pressione qualquer tecla para Voltar", True, (255, 255, 255))

            self.window.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 120))
            self.window.blit(text, (WIN_WIDTH // 2 - text.get_width() // 2, 200))

            pygame.display.flip()
            clock.tick(60)


    def run(self):

        clock = pygame.time.Clock()

        while True:

            # ---------------- EVENTOS ----------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            # ---------------- PLAYER ----------------
            self.player.move()

            # cria magia do player
            if self.player.spawn_magic:
                if self.player.facing_right:
                    magic_x = self.player.rect.x + self.scroll + 55
                else:
                    magic_x = self.player.rect.x + self.scroll - 20

                magic_y = self.player.rect.y + 25

                self.magic_list.append(
                    Magic(magic_x, magic_y, self.player.facing_right)
                )

                self.player.spawn_magic = False

            # atualiza magias do player
            for magic in self.magic_list[:]:
                magic.update()

                if magic.rect.x > 6000 or magic.rect.x < -200:
                    self.magic_list.remove(magic)

            # ---------------- INIMIGO NORMAL ----------------
            if self.enemy:
                self.enemy.move()

            if self.enemy2:
                self.enemy2.move()

            # ---------------- BOSS ---------------
            if self.boss:
                self.boss.move()
                self.boss_attack_timer += 1

                boss_screen_x = self.boss.rect.x - self.scroll
                distance_to_player = abs(self.player.rect.centerx - boss_screen_x)

                # inicia a rajada
                if self.boss_attack_timer > 90 and self.boss_shots == 0 and distance_to_player < 300:
                    self.boss_shots = 3
                    self.boss_shot_delay = 0
                    self.boss_attack_timer = 0

                # dispara as magias uma por uma
                if self.boss_shots > 0:
                    self.boss_shot_delay += 1

                    if self.boss_shot_delay > 20:  # tempo entre cada magia
                        self.boss_shot_delay = 0

                        boss_center_screen = self.boss.rect.x - self.scroll + self.boss.rect.width // 2
                        direction = self.player.rect.centerx > boss_center_screen

                        y_positions = [
                            self.boss.rect.y + 20,
                            self.boss.rect.y + 150,
                            self.boss.rect.y + 280
                        ]

                        y = y_positions[3 - self.boss_shots]

                        self.boss_magic_list.append(
                            Magic(self.boss.rect.x + 40, y, direction)
                        )

                        self.boss_shots -= 1

                        print("Boss lançou uma magia da rajada!")

            # atualiza magias do boss
            for magic in self.boss_magic_list[:]:
                magic.update()

                if magic.rect.x > 6000 or magic.rect.x < -200:
                    self.boss_magic_list.remove(magic)

            # ---------------- INVULNERABILIDADE ----------------
            if self.player.invulnerable:
                self.player.invulnerable_time -= 1

                if self.player.invulnerable_time <= 0:
                    self.player.invulnerable = False

            # ---------------- CÂMERA ----------------
            keys = pygame.key.get_pressed()

            right_limit = WIN_WIDTH * 0.5
            left_limit = WIN_WIDTH * 0.3

            if not self.boss_arena:
                # andar para direita
                if keys[pygame.K_d]:
                    if self.player.rect.centerx > right_limit and self.scroll < self.max_scroll:
                        delta = min(self.player.speed, self.max_scroll - self.scroll)
                        self.scroll += delta
                        self.player.rect.x -= delta

                # andar para esquerda
                if keys[pygame.K_a]:
                    if self.player.rect.centerx < left_limit and self.scroll > 0:
                        delta = min(self.player.speed, self.scroll)
                        self.scroll -= delta
                        self.player.rect.x += delta
            else:
                # arena travada
                self.scroll = self.arena_scroll

            # boss aparece antes do final
            if self.scroll >= self.max_scroll - 700 and not self.boss_spawned:
                print("Boss apareceu!")
                self.boss = EntityFactory.get_entity('Boss', (self.map_width - 420, 100))
                self.boss_spawned = True

            # trava a arena mais perto do final
            if self.boss_spawned and not self.boss_arena and self.scroll >= self.max_scroll - 216:
                print("Arena do boss travada!")
                self.finished = True
                self.boss_arena = True
                self.arena_scroll = self.scroll

                if self.player.rect.right > WIN_WIDTH - 220:
                    self.player.rect.right = WIN_WIDTH - 120

            # trava o player dentro da arena
            if self.boss_arena:
                if self.player.rect.left < 20:
                    self.player.rect.left = 20

                if self.player.rect.right > WIN_WIDTH - 20:
                    self.player.rect.right = WIN_WIDTH - 20

            # ---------------- LIMITES DO MAPA ----------------
            # ---------------- LIMITES DO MAPA ----------------
            world_x = self.player.rect.x + self.scroll

            if world_x < 0:
                self.player.rect.x = -self.scroll

            if world_x + self.player.rect.width > self.map_width:
                self.player.rect.x = self.map_width - self.player.rect.width - self.scroll

            # ---------------- GRAVIDADE ----------------
            self.player.on_ground = False
            previous_bottom = self.player.rect.bottom
            self.player.apply_gravity()

            # colisão com paredes invisíveis
            for wall in self.walls:
                wall_rect = pygame.Rect(wall.x - self.scroll, wall.y, wall.width, wall.height)

                if self.player.rect.colliderect(wall_rect):
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_d] and self.player.rect.centerx < wall_rect.centerx:
                        self.player.rect.right = wall_rect.left

                    elif keys[pygame.K_a] and self.player.rect.centerx > wall_rect.centerx:
                        self.player.rect.left = wall_rect.right
                    # parede horizontal
                    else:

                        # batendo a cabeça
                        if self.player.gravity < 0:
                            self.player.rect.top = wall_rect.bottom
                            self.player.gravity = 0

                        # caindo em cima
                        elif self.player.gravity >= 0:
                            self.player.rect.bottom = wall_rect.top
                            self.player.gravity = 0
                            self.player.on_ground = True

            # colisão com plataformas
            for p in self.platforms:
                rect = pygame.Rect(p.x - self.scroll, p.y, p.width, p.height)

                if self.player.rect.colliderect(rect) and self.player.gravity >= 0:
                    if previous_bottom <= rect.top and rect.left + 5 < self.player.rect.centerx < rect.right - 5:
                        self.player.rect.bottom = rect.top
                        self.player.gravity = 0
                        self.player.on_ground = True

            # ---------------- HITBOX PLAYER ----------------
            player_hitbox = pygame.Rect(
                self.player.rect.x + 10,
                self.player.rect.y + 5,
                40,
                60
            )

            # ---------------- COLISÃO COM INIMIGO ----------------
            enemy_hitbox = None

            if self.enemy:
                enemy_hitbox = pygame.Rect(
                    self.enemy.rect.x - self.scroll + 9,
                    self.enemy.rect.y + 7,
                    35,
                    50
                )

                # player encostou no inimigo
                if player_hitbox.colliderect(enemy_hitbox) and not self.player.invulnerable:
                    self.player.life -= 1
                    self.player.invulnerable = True
                    self.player.invulnerable_time = 60
                    self.player.rect.topleft = (50, 200)
                    self.scroll = 0

                    print(f"Vida: {self.player.life}")

                # magia acertou inimigo
                for magic in self.magic_list[:]:
                    magic_hitbox = pygame.Rect(
                        magic.rect.x - self.scroll,
                        magic.rect.y,
                        magic.rect.width,
                        magic.rect.height
                    )

                    if magic_hitbox.colliderect(enemy_hitbox):
                        self.magic_list.remove(magic)
                        self.enemy.life -= 1

                        print("Magia acertou o inimigo!")

                        if self.enemy.life <= 0:
                            print("Inimigo morreu")
                            self.enemy = None
                            break

            if self.enemy2:
                enemy2_hitbox = pygame.Rect(
                    self.enemy2.rect.x - self.scroll + 9,
                    self.enemy2.rect.y + 7,
                    35,
                    50
                )

                # player encostou no inimigo 2
                if player_hitbox.colliderect(enemy2_hitbox) and not self.player.invulnerable:
                    self.player.life -= 1
                    self.player.invulnerable = True
                    self.player.invulnerable_time = 60
                    self.player.rect.topleft = (50, 200)
                    self.scroll = 0

                    print(f"Vida: {self.player.life}")

                # magia acertou inimigo 2
                for magic in self.magic_list[:]:
                    magic_hitbox = pygame.Rect(
                        magic.rect.x - self.scroll,
                        magic.rect.y,
                        magic.rect.width,
                        magic.rect.height
                    )

                    if magic_hitbox.colliderect(enemy2_hitbox):
                        self.magic_list.remove(magic)
                        self.enemy2.life -= 1

                        print("Magia acertou o inimigo 2!")

                        if self.enemy2.life <= 0:
                            print("Inimigo 2 morreu")
                            self.enemy2 = None
                            break

            # ---------------- COLISÃO COM BOSS ----------------
            if self.boss:
                boss_hitbox = pygame.Rect(
                    self.boss.rect.x - self.scroll + 20,
                    self.boss.rect.y + 20,
                    self.boss.rect.width - 40,
                    self.boss.rect.height - 40
                )

                # impede o player de atravessar o boss
                if player_hitbox.colliderect(boss_hitbox):
                    if self.player.facing_right:
                        self.player.rect.right = boss_hitbox.left
                    else:
                        self.player.rect.left = boss_hitbox.right

                # magia do boss acertou o player
                for magic in self.boss_magic_list[:]:
                    magic_hitbox = pygame.Rect(
                        magic.rect.x - self.scroll,
                        magic.rect.y,
                        magic.rect.width,
                        magic.rect.height
                    )

                    if magic_hitbox.colliderect(player_hitbox) and not self.player.invulnerable:
                        self.boss_magic_list.remove(magic)
                        self.player.life -= 1
                        self.player.invulnerable = True
                        self.player.invulnerable_time = 60

                        print("Player levou dano do boss!")

                # player encostou no boss
                if player_hitbox.colliderect(boss_hitbox) and not self.player.invulnerable:
                    self.player.life -= 1
                    self.player.invulnerable = True
                    self.player.invulnerable_time = 60

                    print(f"Vida: {self.player.life}")

                # magia do player acertou o boss
                for magic in self.magic_list[:]:
                    magic_hitbox = pygame.Rect(
                        magic.rect.x - self.scroll,
                        magic.rect.y,
                        magic.rect.width,
                        magic.rect.height
                    )

                    if magic_hitbox.colliderect(boss_hitbox):
                        self.magic_list.remove(magic)
                        self.boss.life -= 1

                        print("Magia acertou o boss!")

                       #TELA PRA WINS
                        if self.boss.life <= 0:
                            print("Boss derrotado!")
                            self.boss = None
                            self.show_end_screen("WINS!")
                            return "WINS!"

            # ---------------- GAME OVER ----------------
            if self.player.life <= 0:
                print("GAME OVER")
                self.show_end_screen("GAME OVER")
                return "GAME OVER"


            # ---------------- DESENHO ----------------
            self.window.fill((0, 0, 0))

            bg1_width = self.bg1.get_width()
            bg2_width = self.bg2.get_width()
            bg3_width = self.bg3.get_width()

            self.window.blit(self.bg0, (0, 0))

            cloud_y = -50
            self.window.blit(self.bg1, ((-self.scroll * 0.2) % bg1_width - bg1_width, cloud_y))
            self.window.blit(self.bg1, ((-self.scroll * 0.2) % bg1_width, cloud_y))

            forest_y = self.ground_y - 330
            self.window.blit(self.bg2, ((-self.scroll * 0.6) % bg2_width - bg2_width, forest_y))
            self.window.blit(self.bg2, ((-self.scroll * 0.6) % bg2_width, forest_y))

            ground_visual_y = self.ground_y - 280
            self.window.blit(self.bg3, ((-self.scroll * 0.8) % bg3_width - bg3_width, ground_visual_y))
            self.window.blit(self.bg3, ((-self.scroll * 0.8) % bg3_width, ground_visual_y))



            for p in self.platforms[1:]:
                rect = pygame.Rect(p.x - self.scroll, p.y, p.width, p.height)
                platform_scaled = pygame.transform.scale(self.platform_img, (p.width, p.height))
                self.window.blit(platform_scaled, rect)

            # inimigo
            if self.enemy:
                enemy_draw_rect = pygame.Rect(
                    self.enemy.rect.x - self.scroll,
                    self.enemy.rect.y,
                    self.enemy.rect.width,
                    self.enemy.rect.height
                )

                self.window.blit(self.enemy.surf, enemy_draw_rect)
               # pygame.draw.rect(self.window, (255, 0, 0), enemy_hitbox, 2)

            if self.enemy2:
                enemy2_draw_rect = pygame.Rect(
                    self.enemy2.rect.x - self.scroll,
                    self.enemy2.rect.y,
                    self.enemy2.rect.width,
                    self.enemy2.rect.height
                )

                self.window.blit(self.enemy2.surf, enemy2_draw_rect)
               # pygame.draw.rect(self.window, (255, 0, 0), enemy2_hitbox, 2)

            # boss
            if self.boss:
                boss_draw_rect = pygame.Rect(
                    self.boss.rect.x - self.scroll,
                    self.boss.rect.y,
                    self.boss.rect.width,
                    self.boss.rect.height
                )

                self.window.blit(self.boss.surf, boss_draw_rect)
               # pygame.draw.rect(self.window, (255, 0, 0), boss_hitbox, 2)

            # magias
            for magic in self.magic_list:
                self.window.blit(magic.surf, (magic.rect.x - self.scroll, magic.rect.y))

            for magic in self.boss_magic_list:
                self.window.blit(magic.surf, (magic.rect.x - self.scroll, magic.rect.y))

            # player
            self.window.blit(self.player.surf, self.player.rect)

            for wall in self.walls:
                wall_rect = pygame.Rect(wall.x - self.scroll, wall.y, wall.width, wall.height)
                #pygame.draw.rect(self.window, (0, 255, 0), wall_rect, 2)

            pygame.display.flip()
            clock.tick(60)