# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 21:42:39 2020

@author: Christian Konstantinov
"""

import pygame as pg
from scene import Scene, Button
from pygame import mixer

class Settings(Scene):
    def __init__(self, surface, color, font=None, bgi=None, bgm=None):
        super().__init__(surface, color, font=font, bgi=bgi, bgm=bgm)
        self.colors =  {'idle': (0xA0,0xB6,0xBD),
                       'hover': (0x8E,0xBA,0xC8),
                       'press': (0x79,0x8A,0x8F)
                       }
        self.font = font
        self.menuback = mixer.Sound('assets/audio/menuback.wav')

    def update(self):
        pass

    def render(self):
        self.surface.fill(self.color)
        self.surface.blit(self.font.render(
                'Settings', False, (0,0,0)),
                (self.width/2, self.height/6))
        #pg.display.flip()

    def handle_event(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            self.menuback.play()
            self.change_scene('title')