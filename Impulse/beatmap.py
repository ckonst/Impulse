import json
import os
from pathlib import Path

import pygame as pg

from Impulse.events import Event
from Impulse.mapgen import mapgen
from Impulse.scene.map import Map

import logging as log


class BeatMapManager():

    def __init__(self, clock, surface, bg_color, font):
        self.clock = clock
        self.beatmaps = {}
        self.BEATMAPS_PATH = './Impulse/data/beatmaps/'
        self.surface = surface
        self.bg_color = bg_color
        self.font = font
        self.load_maps()

    def load_maps(self):
        """Load each beatmap into a Map object and storing it into the beatmaps dict."""
        folders = os.listdir(self.BEATMAPS_PATH)
        for name in folders:
            path = f'{self.BEATMAPS_PATH}{name}/{name}'
            with open(f'{self.BEATMAPS_PATH}{name}/beatmap.json') as f:
                beatmap = json.load(f)
            if os.path.exists(path + '.jpg'):
                img = path + '.jpg'
            elif os.path.exists(path + '.png'):
                img = path + '.png'
            else:
                img = None
            self.beatmaps[name] = Map(
                self.surface,
                self.bg_color,
                name,
                beatmap,
                self.clock,
                font=self.font,
                reload=self.reload,
                bgi=img,
                bgm=path + '.mp3',
            )

    def load_map(self, name):
        """Load the beatmap's assets. Called before changing the scene."""
        self.reload(name)  # make sure this
        audio_path = self.beatmaps[name].bgm
        pg.mixer.music.load(audio_path)
        img_path = self.beatmaps[name].bgi
        if img_path:
            pg.image.load(img_path)

    def reload(self, name):
        old: Map = self.beatmaps[name]
        self.beatmaps[name] = Map(
            self.surface,
            self.bg_color,
            name,
            old.beatmap,
            self.clock,
            reload=self.reload,
            font=self.font,
            bgi=old.bgi,
            bgm=old.bgm,
        )
        self._post_update_event(name)

    def generate_beatmap(self):
        """Generate a beatmap, called when a button's onclick action is called in Map Select."""
        beatmap = mapgen.generate()
        if beatmap is None:
            return False
        name = beatmap['name']
        path = f'{self.BEATMAPS_PATH}{name}/{name}'
        self.beatmaps[name] = Map(
            self.surface,
            self.bg_color,
            name,
            beatmap,
            self.clock,
            font=self.font,
            bgi=None,
            bgm=f'{path}.mp3',
        )
        self._post_update_event(name)

    def _post_update_event(self, name):
        pg.event.post(
            pg.event.Event(
                Event.BEATMAP_UPDATE_EVENT,
                event_name=name,
                beatmap=self.beatmaps[name],
            ))
