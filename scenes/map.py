# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 21:44:03 2020

@author: Christian Konstantinov
"""

import pygame as pg
from scene import Scene

class Map(Scene):
    def __init__(self, window, beatmap, running=True, font=None, bgi=None, bgm=None):
        super.__init__(self, window, running, font, bgi, bgm)
        self.beatmap = beatmap
    def update(self):
        pass
    def render(self):
        pass