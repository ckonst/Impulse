import os
import json
from scenes.map import Map
import pygame as pg
from mapgen import mapgen
from event import Event

class BeatMapManager():
    def __init__(self, clock, surface, bg_color, font):
        self.clock = clock
        self.beatmaps = {}
        self.BEATMAPS = './beatmaps/'
        self.surface = surface
        self.bg_color = bg_color
        self.font = font
        self.load_maps()

    def load_maps(self):
        folders = os.listdir(self.BEATMAPS)
        for name in folders:
            path = f'{self.BEATMAPS}{name}/{name}'
            with open(f'{self.BEATMAPS}{name}/beatmap.json') as f:
                beatmap = json.load(f)
            if os.path.exists(f'{path}.jpg'):
                img = f'{path}.jpg'
            elif os.path.exists(f'{path}.png'):
                img = f'{path}.png'
            else:
                img = None
            self.beatmaps[name] = Map(self.surface, self.bg_color, name, beatmap,
                                      self.clock, font=self.font, bgi=img,
                                      bgm=f'{path}.mp3')

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
        path = f'{self.BEATMAPS}{name}/{name}'
        self.beatmaps[name] = Map(surface, bg_color, name, beatmap, self.clock, font=font,
                                  bgi=None, bgm=f'{path}.mp3')
        pg.event.post(pg.event.Event(Event.BEATMAP_UPDATE_EVENT,
                                     event_name=name, beatmap=self.beatmaps[name]))