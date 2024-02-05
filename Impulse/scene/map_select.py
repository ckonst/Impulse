import pygame as pg
from pygame import mixer

from Impulse.events import Event
from Impulse.scene import Scene
from Impulse.scene.buttons import ButtonState, RectangleButton

import logging as log


class MapSelect(Scene):

    def __init__(self, surface, color, beat_manager, font=None, bgi=None, bgm=None):
        super().__init__(surface, color, font=font, bgi=bgi, bgm=bgm)
        self.beat_manager = beat_manager
        self.beatmaps = beat_manager.beatmaps
        self.w = 800
        self.h = 100
        self.colors = {
            ButtonState.IDLE: (0xA0, 0xB6, 0xBD),
            ButtonState.HOVER: (0x8E, 0xBA, 0xC8),
            ButtonState.PRESS: (0x79, 0x8A, 0x8F)
        }
        self.menu_items = [
            RectangleButton(
                name,
                self.surface,
                self.play_map,
                self.width // 2 - self.w // 2,
                self.height // 2 - self.h // 1.5 + 150 * i,
                self.w,
                self.h,
                self.colors,
                font=font,
                is_song=True,
            ) for i, name in enumerate(self.beatmaps.keys())
        ]
        self.menu_items.append(
            RectangleButton(
                'Import',
                self.surface,
                self.beat_manager.generate_beatmap,
                0,
                0,
                self.w / 2,
                self.h,
                self.colors,
                font=self.font,
                movable=False,
            ))

    def update(self):
        if mixer.music.get_busy():
            mixer.music.unload()
        for button in self.menu_items:
            button.update()

    def render(self):
        self.surface.fill(self.color)
        for button in self.menu_items:
            button.render()

    def handle_event(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            # go back
            self.menuback.play()
            self.change_scene('title')
        elif e.type == pg.MOUSEWHEEL:
            # scroll
            for button in self.menu_items:
                if button.movable:
                    pg.time.wait(1)
                    button.dy = e.y * 15
        elif e.type == Event.BEATMAP_UPDATE_EVENT:
            # play map
            log.debug(f'Handling Beatmap Update of {e.event_name} in Map Select')
            self.beatmaps.update({e.event_name: e.beatmap})
        else:
            for button in self.menu_items:
                button.handle_event(e)

    def play_map(self, name):
        self.beat_manager.load_map(name)
        self.change_scene(name)
