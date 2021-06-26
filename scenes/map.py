# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 21:44:03 2020

@author: Christian Konstantinov
"""

import pygame as pg
from pygame import mixer
from scene import Scene, Button
from pygame import time
from event import Event

class Map(Scene):
    def __init__(self, surface, color, name, beatmap, game_clock, font=None, bgi=None, bgm=None):
        super().__init__(surface, color, font=font, bgi=bgi, bgm=bgm)
        self.img = pg.image.load('./assets/img/button30.png')
        self.name = name
        self.beatmap = beatmap
        self.beats = beatmap['onsets']
        w, h = surface.get_size()
        img_w, img_h = self.img.get_size()
        self.xs = map(lambda x: round((x + 1) / 2 * (w - img_w)), beatmap['xs'])
        self.ys = map(lambda y: round((y + 1) / 2 * (h - img_h)), beatmap['ys'])
        self.bmr = self._beatmap_reader()
        self.finished = False
        self.clock = time.Clock()
        self.game_clock = game_clock
        self.c_x = self.beatmap['xs'][0] # current x position
        self.c_y = self.beatmap['ys'][0] # current y position
        self.c_beat = self.beats[0] # current beat in seconds
        self.buttons = [] # current buttons on screen
        self.counter = 0 # counter for button text
        self.last_note = 0 # last number note hit
        self.time = -3
        self.error = 0.005
        self.offset = 0.5
        self.score = 0
        self.combo = 0
        self.total_misses = 0
        self.failure_condition = 50
        self.circlehit = mixer.Sound('./assets/audio/circlehit.mp3')
        self.circlehit.set_volume(0.5)
        self.menuback = mixer.Sound('assets/audio/menuback.wav')
        self.waiting = False
        self.holding = False

    def update(self):
        if not mixer.music.get_busy() and not self.finished:
            if (self.time >= 0):
                mixer.music.play()

        if self.finished:
            self.reset()
            self.change_scene('map_select')

        self.clock.tick()
        self.time += self.clock.get_time() / 1000 # get time in seconds.

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
        self.surface.blit(self.font.render(
            f'SCORE: {self.score}', False, (0,0,0)),
            (self.width//2.35, 20))
        self.surface.blit(self.font.render(
            f'{self.combo}X', False, (0,0,0)),
            (20, 1000))
        self.surface.blit(self.font.render(
            f'MISS: {self.total_misses}', False, (0,0,0)),
            (1700, 1000))

    def handle_event(self, e):
        if e.type == Event.COMBO_BREAK_EVENT:
            self.combo = 0
            self.total_misses += 1
            self.last_note = (self.last_note % 8) + 1
            if self.total_misses >= self.failure_condition:
                self.reset()
                self.change_scene('map_select')
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                self.reset()
                self.menuback.play()
                self.change_scene('map_select')
            elif e.key == pg.K_r:
                self.restart()
            elif not self.holding:
                for button in self.buttons:
                    button.handle_event(e)
                self.holding = True
        elif e.type == pg.KEYUP:
            self.holding = False

    def reset(self):
        self.c_x = self.beatmap['xs'][0] # current x position
        self.c_y = self.beatmap['ys'][0] # current y position
        self.c_beat = self.beats[0] # current beat in seconds
        self.buttons = [] # current buttons on screen
        w, h = self.surface.get_size()
        self.xs = map(lambda x: round((x + 1) / 2 * w), self.beatmap['xs'])
        self.ys = map(lambda y: round((y + 1) / 2 * h), self.beatmap['ys'])
        self.clock = time.Clock()
        self.finished = False
        self.counter = 0 # counter for button text
        self.time = -3
        self.score = 0
        self.combo = 0
        self.total_misses = 0
        self.waiting = False
        self.holding = False
        self.last_note = 1 # last number note hit
        for _ in self.bmr:
            pass
        self.bmr = self._beatmap_reader()

    def restart(self):
        self.reset()
        mixer.music.rewind()

    def _beatmap_reader(self):
        for b, x, y in zip(self.beats, self.xs, self.ys):
            yield b, x, y

    def _produce_beat(self, x, y, t):
        self.counter = (self.counter % 8) + 1
        w, h = self.img.get_size()
        button = CircleButton(str(self.counter), self.surface,
                        {'onclick': lambda x: self.hit(x)},
                        self.c_x - w // 2, self.c_y - h // 2,
                        w, h, self.time, self.c_beat, self.game_clock,
                        img=self.img, font=self.font,
                        disappear_after=0.5, num=self.counter)
        self.buttons.insert(0, button)

    def hit(self, circle_button):
        if not circle_button.num == self.last_note + 1:
            return
        self.circlehit.play()
        self.combo += 1
        self.score += 300 * self.combo
        self.last_note = (self.last_note + 1) % 8
        circle_button.visible = False
        self.buttons = [button for button in self.buttons if button is not circle_button]

class CircleButton(Button):
    def __init__(self, text, surface, action, x, y, w, h, t, onset,
                 game_clock, colors=None, img=None, font=None,
                 movable=False, disappear_after=0, num=1):
        super().__init__(text, surface, action, x, y, w, h, colors,
                         img=img, font=font, movable=movable)
        self.disappear_after = disappear_after
        self.clock = time.Clock()
        self.game_clock = game_clock
        self.time = t
        self.onset = onset
        self.tolerance = 0.3 # how far off the onset will we consider a click to be a hit
        self.visible = True
        self.center = (self.x + self.w/2, self.y + self.h/2)
        self.approach_radius = self.w * 2
        self.approach_shrink_rate = ((self.w * 2 - self.w / 2) \
                 / ((onset - t) * game_clock.get_fps()))
        self.num = num

    def update(self):
        if not self.visible:
            return
        self.clock.tick()
        self.time += self.clock.get_time() / 1000 # get time in seconds.
        if self.time >= self.onset + self.disappear_after:
            self.visible = False
            combo_break_event = pg.event.Event(Event.COMBO_BREAK_EVENT)
            pg.event.post(combo_break_event)

    def render(self):
        if not self.visible:
            return
        w, h = self.font.size(self.text)
        self.approach_radius -= self.approach_shrink_rate
        pg.draw.circle(self.surface, 0xffffff, self.center, self.approach_radius, width=10)
        self.surface.blit(self.img, (self.x, self.y))
        self.surface.blit(self.font.render(
        self.text, False, (0,0,0)),
        (self.x + self.w/2 - w/2, self.y + self.h/2 - h/2))

    def handle_event(self, e):
        if e.key == pg.K_z or pg.K_x:
            self.check_hovering()
            if self.hovering:
                low = self.onset - self.tolerance
                high = self.onset + self.tolerance
                if self.time >= low and self.time <= high:
                    self.action['onclick'](self)
