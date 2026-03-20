#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import pygame

from code.Const import WIN_HEIGHT, WIN_WIDTH, MENU_OPTION
from code.level import Level
from code.menu import Menu


class Game:
    def __init__(self, ):
        self.window = None
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    def run(self,):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]: # novo jogo
                level = Level(self.window, 'Level1', menu_return)
                level.run()

            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                sys.exit() #end game
            else:
                pass



