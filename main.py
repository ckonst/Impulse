# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:13:05 2020

@author: Christian Konstantinov
"""

import pygame as pg
from scenes.map import Map
from scenes.scene import SceneManager
from scenes.title import Title
from scenes.settings import Settings
from scenes.map_select import MapSelect
import events
from mapgen import mapgen
import os
import json

pg.init() # init everything

# display stuff
width = 1920
height = 1080
surface = pg.display.set_mode([width, height])
surface.convert()
bg_color = 0x343B3D
cursor = pg.image.load('./assets/img/cursor.png')
pg.mouse.set_visible(False)

def render_cursor():
    x, y = pg.mouse.get_pos()
    w, h = cursor.get_size()
    surface.blit(cursor, (x - w // 2, y - w // 2))

# font stuff
FONT_PATH = './assets/fonts/Gidole-Regular.otf'
font = pg.font.Font(FONT_PATH, 48)

BEATMAPS = './beatmaps/'

class BeatMapManager():
    def __init__(self):
        self.beatmaps = {}
        self.load_maps()

    def load_maps(self):
        folders = os.listdir(BEATMAPS)
        for name in folders:
            path = f'{BEATMAPS}{name}/{name}'
            with open(f'{BEATMAPS}{name}/beatmap.json') as f:
                beatmap = json.load(f)
            if os.path.exists(f'{path}.jpg'):
                img = f'{path}.jpg'
            elif os.path.exists(f'{path}.png'):
                img = f'{path}.png'
            else:
                img = None
            self.beatmaps[name] = Map(surface, bg_color, name, beatmap, font=font,
                                  bgi=img, bgm=f'{path}.mp3')

    def load_map(self, name):
        audio_path = self.beatmaps[name].bgm
        pg.mixer.music.load(audio_path)
        img_path = self.beatmaps[name].bgi
        if img_path:
            pg.image.load(img_path)

    def generate_beatmap(self):
        beatmap = mapgen.generate()
        if not beatmap:
            return False
        name = beatmap['name']
        path = f'{BEATMAPS}{name}/{name}'
        self.beatmaps[name] = Map(surface, bg_color, name, beatmap, font=font,
                                  bgi=None, bgm=f'{path}.mp3')
        pg.event.post(pg.event.Event(events.BEATMAP_UPDATE_EVENT,
                                     event_name=name, beatmap=self.beatmaps[name]))

beat_manager = BeatMapManager()

scenes = {'title': Title(surface, bg_color, font=font),
          'settings': Settings(surface, bg_color, font=font),
          'map_select': MapSelect(surface, bg_color, beat_manager, font=font),
          **beat_manager.beatmaps}

manager = SceneManager(scenes, scenes['title'])

running = True

#%% GAME LOOP

while running:
    try:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                break
            elif e.type == events.BEATMAP_UPDATE_EVENT:
                manager.scenes[e.event_name] = beat_manager.beatmaps[e.event_name]
                manager.current_scene.handle_event(e)
            elif e.type == events.SCENE_CHANGE_EVENT:
                manager.current_scene = manager.scenes[e.event_name]
            else:
                manager.current_scene.handle_event(e)

        manager.update()
        manager.render()
        render_cursor()
        pg.display.flip()
    except KeyboardInterrupt:
        break
pg.quit()