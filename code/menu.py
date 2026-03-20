#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import pygame.image
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, MENU_OPTION, COLOR_PINK, COLOR_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/MenuBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer.music.load('./assets/Menu.mp3')
        pygame.mixer.music.play(-1)
        while True:
            # DRAW IMAGES
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(15, "RU: 4101339", COLOR_WHITE, (60, 20))
            self.menu_text(50, "Plantas", COLOR_WHITE, ((WIN_WIDTH / 2), 30))
            self.menu_text(50, "Aliens", COLOR_WHITE, ((WIN_WIDTH / 2), 80))
            self.menu_text(50, "Demo", COLOR_WHITE, ((WIN_WIDTH / 2), 130))

            self.menu_text(16, "Comandos para jogar", COLOR_WHITE, (110, 200))
            self.menu_text(15, "W - Pula", COLOR_WHITE, (100, 240))
            self.menu_text(15, "A - Esquerda", COLOR_WHITE, (100, 260))
            self.menu_text(15, "D - Direita", COLOR_WHITE, (100, 280))
            self.menu_text(15, "C - Ataque", COLOR_WHITE, (100, 300))

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(25, MENU_OPTION[i], COLOR_PINK, ((WIN_WIDTH / 2), 200 + 25 * i))
                else:
                    self.menu_text(25, MENU_OPTION[i], COLOR_WHITE, ((WIN_WIDTH / 2), 200 + 25 * i))
            pygame.display.flip()

                     #check for all events
            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:  # DOWN KEY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:  # UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:  # ENTER
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
