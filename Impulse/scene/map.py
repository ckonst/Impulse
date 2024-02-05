from typing import Callable
import pygame as pg
from pygame import mixer, time

import logging as log
from Impulse.events import Event
from Impulse.scene import Scene
from Impulse.scene.buttons import CircleButton


class Map(Scene):

    def __init__(
        self,
        surface,
        color,
        name,
        beatmap,
        game_clock,
        reload=lambda _: ...,
        font=None,
        bgi=None,
        bgm=None,
    ):
        super().__init__(surface, color, font=font, bgi=bgi, bgm=bgm)
        self.img = pg.image.load('./Impulse/data/assets/img/button30.png')
        self.name = name
        self.beatmap = beatmap
        self.onsets = beatmap['onsets']
        w, h = surface.get_size()
        img_w, img_h = self.img.get_size()
        self.xs = [round((x + 1) / 2 * (w - img_w)) for x in beatmap['xs']]
        self.ys = [round((y + 1) / 2 * (h - img_h)) for y in beatmap['ys']]
        self.bmr = self._beatmap_reader()
        self.finished = False
        self.clock = time.Clock()
        self.game_clock = game_clock
        self.reload: Callable[[], None] = reload
        self.c_x = self.beatmap['xs'][0]  # current x position
        self.c_y = self.beatmap['ys'][0]  # current y position
        self.c_beat = self.onsets[0]  # current beat in seconds
        self.buttons = []  # current buttons on screen
        self.counter = 0  # counter for button text
        self.last_note = 0  # last number note hit
        self.time = -3  # start time
        self.error = 0.005
        self.offset = 0.5
        self.score = 0
        self.combo = 0
        self.total_misses = 0
        self.failure_condition = 50
        self.waiting = False
        self.holding = False

    def update(self):
        if not mixer.music.get_busy() and not self.finished:
            if (self.time >= 0):
                mixer.music.play()

        self.clock.tick()
        self.time += self.clock.get_time() / 1000  # get time in seconds.

        low = self.c_beat - self.error - self.offset
        high = self.c_beat + self.error - self.offset

        if not self.waiting:
            try:
                self.c_beat, self.c_x, self.c_y = next(self.bmr)
            except StopIteration:
                self.finished = True
        if self.time >= low and self.time <= high:
            self._produce_beat(self.c_x, self.c_y, self.c_beat)
            self.waiting = False
        else:
            self.waiting = True

        for button in self.buttons:
            button.update()
        self.buttons = [button for button in self.buttons if button.visible]

    def render(self):
        self.surface.fill(self.color)
        for button in self.buttons:
            button.render()
        self.surface.blit(
            self.font.render(f'SCORE: {self.score}', False, (0, 0, 0)),
            (self.width // 2.35, 20),
        )
        self.surface.blit(
            self.font.render(f'{self.combo}X', False, (0, 0, 0)),
            (20, 1000),
        )
        self.surface.blit(
            self.font.render(f'MISS: {self.total_misses}', False, (0, 0, 0)),
            (1700, 1000),
        )

    def handle_event(self, e):
        match (e.type):
            case Event.COMBO_BREAK_EVENT:
                self.combo = 0
                self.total_misses += 1
                self.last_note = (self.last_note % 8) + 1
                if self.total_misses >= self.failure_condition:
                    self.change_scene('map_select')
                    self.reload(self.name)
            case pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.finished = True
                    self.menuback.play()
                    # Change scene before reload to ensure BEATMAP_UPDATE_EVENT is handled in MapSelect.
                    self.change_scene('map_select')
                    self.reload(self.name)
                elif e.key == pg.K_r:
                    self.finished = True
                    self._restart()
                elif not self.holding:
                    for button in self.buttons:
                        button.handle_event(e)
                    self.holding = True
            case pg.KEYUP:
                self.holding = False

    def _restart(self):
        # Reload before changing scene to ensure BEATMAP_UPDATE_EVENT is handled before resetting the scene.
        self.reload(self.name)
        self.change_scene(self.name)
        mixer.music.rewind()
        mixer.music.stop()

    def _beatmap_reader(self):
        for o, x, y in zip(self.onsets, self.xs, self.ys):
            yield o, x, y

    def _produce_beat(self, x, y, t):
        self.counter = (self.counter % 8) + 1
        w, h = self.img.get_size()
        button = CircleButton(
            str(self.counter),
            self.surface,
            lambda x: self._hit(x),
            self.c_x - w // 2,
            self.c_y - h // 2,
            w,
            h,
            self.time,
            self.c_beat,
            self.game_clock,
            img=self.img,
            font=self.font,
            disappear_after=0.5,
            num=self.counter,
        )
        self.buttons.insert(0, button)

    def _hit(self, circle_button):
        if not circle_button.num == self.last_note + 1:
            return
        circle_button.sound.play()
        self.combo += 1
        self.score += 300 * self.combo
        self.last_note = (self.last_note + 1) % 8
        circle_button.visible = False
        self.buttons = [button for button in self.buttons if button is not circle_button]
