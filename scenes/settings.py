# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 21:42:39 2020

@author: Christian Konstantinov
"""

import pygame as pg
from scene import Scene

class Settings(Scene):
    def __init__(self, window, running=True, font=None, bgi=None, bgm=None):
        super.__init__(self, window, running, font, bgi, bgm)
        self.menu_items = [
            {
                'name': 'Play',
                'action': lambda: self.to_map_select()
            },
            {
                'name': 'Settings',
                'action': lambda: self.to_settings()
            },
            {
                'name': 'Quit',
                'action': lambda: self.quit_game()
            }
        ]
    def update(self):
        pass
    def render(self):
        pass