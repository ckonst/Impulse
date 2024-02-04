import pygame as pg
from buttons import RectangleButton
from events import Event
from pygame import mixer
from scene import Scene


class MapSelect(Scene):

    def __init__(self, surface, color, beat_manager, font=None, bgi=None, bgm=None):
        super().__init__(surface, color, font=font, bgi=bgi, bgm=bgm)
        self.beat_manager = beat_manager
        self.beatmaps = beat_manager.beatmaps
        self.w = 800
        self.h = 100
        x = self.width // 2 - self.w // 2
        y = self.height // 2 - self.h // 1.5
        keys = self.beatmaps.keys()
        self.colors = {
            'idle': (0xA0, 0xB6, 0xBD),
            'hover': (0x8E, 0xBA, 0xC8),
            'press': (0x79, 0x8A, 0x8F)
        }
        self.menu_items = [
            RectangleButton(name,
                            self.surface,
                            self.play_map,
                            x,
                            y + 150 * i,
                            self.w,
                            self.h,
                            self.colors,
                            font=font,
                            is_song=True) for i, name in enumerate(keys)
        ]
        gen = self.beat_manager.generate_beatmap
        self.menu_items.append(
            RectangleButton('Import',
                            self.surface,
                            gen,
                            0,
                            0,
                            self.w / 2,
                            self.h,
                            self.colors,
                            font=self.font,
                            movable=False))

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
            self.beatmaps.update({e.event_name: e.beatmap})
            self.play_map(e.event_name)
        else:
            for button in self.menu_items:
                button.handle_event(e)

    def play_map(self, name):
        self.beat_manager.load_map(name)
        self.change_scene(name)
