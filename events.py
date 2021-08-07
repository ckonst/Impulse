# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 00:12:01 2020

@author: Christian Konstantinov
"""

import pygame as pg

from enum import IntEnum

class Event(IntEnum):
    SCENE_CHANGE_EVENT = pg.USEREVENT+1
    BEATMAP_UPDATE_EVENT = pg.USEREVENT+2
    COMBO_BREAK_EVENT = pg.USEREVENT+3