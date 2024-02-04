from enum import IntEnum

import pygame as pg


class Event(IntEnum):
    SCENE_CHANGE_EVENT = pg.USEREVENT + 1
    BEATMAP_UPDATE_EVENT = pg.USEREVENT + 2
    COMBO_BREAK_EVENT = pg.USEREVENT + 3
