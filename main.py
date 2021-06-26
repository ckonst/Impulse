# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:13:05 2020

@author: Christian Konstantinov
"""

import pygame as pg
from beatmap import BeatMapManager
from scenes.scene import SceneManager
from scenes.title import Title
from scenes.settings import Settings
from scenes.map_select import MapSelect
from event import Event

def main():
    pg.init() # init everything

    # display stuff
    width = 1920
    height = 1080
    surface = pg.display.set_mode([width, height])
    surface.convert()
    bg_color = 0x343B3D
    cursor = pg.image.load('./assets/img/cursor.png')
    pg.mouse.set_visible(False)

    FONT_PATH = './assets/fonts/Gidole-Regular.otf'
    font = pg.font.Font(FONT_PATH, 48)
    clock = pg.time.Clock()
    beat_manager = BeatMapManager(clock, surface, bg_color, font)

    scenes = {'title': Title(surface, bg_color, font=font),
            'settings': Settings(surface, bg_color, font=font),
            'map_select': MapSelect(surface, bg_color, beat_manager, font=font),
            **beat_manager.beatmaps}

    manager = SceneManager(scenes, scenes['title'], surface, cursor)

    running = True

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                break
            elif e.type == Event.BEATMAP_UPDATE_EVENT:
                manager.scenes[e.event_name] = beat_manager.beatmaps[e.event_name]
                manager.current_scene.handle_event(e)
            elif e.type == Event.SCENE_CHANGE_EVENT:
                manager.current_scene = manager.scenes[e.event_name]
            else:
                manager.current_scene.handle_event(e)
        manager.update()
        manager.render()
        pg.display.update()
        clock.tick(240)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pg.quit()