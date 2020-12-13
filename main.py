# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:13:05 2020

@author: Christian Konstantinov
"""

import pygame as pg
from pygame.locals import *
from scenes.scene import SceneManager
import events

pg.init()

width = 1920
height = 1080
screen = pg.display.set_mode([width, height])

manager = SceneManager([], None)

#%% GAME LOOP
running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
            break
        if e.type == events.SCENE_CHANGE_EVENT:
            manager.current_scene = manager.scenes[e.event_name]
            manager.current_scene.handle_event(e)

    manager.update()
    manager.render()

    screen.fill((0xff,0xff,0xff))
    pg.draw.circle(screen, (0,0,0xff), (width//2, height//2), 75)
    pg.display.flip()

pg.quit()