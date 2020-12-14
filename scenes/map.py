# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 21:44:03 2020

@author: Christian Konstantinov
"""

import pygame as pg
from pygame import mixer
from scene import Scene, Button
from pygame import time
import events

class Map(Scene):
    def __init__(self, surface, color, name, beatmap, font=None, bgi=None, bgm=None):
        super().__init__(surface, color, font=font, bgi=bgi, bgm=bgm)
        self.img = pg.image.load('./assets/img/button30.png')
        self.name = name
        self.beatmap = beatmap
        self.beats = beatmap['onsets']
        w, h = surface.get_size()
        self.xs = map(lambda x: round((x + 1) / 2 * w), beatmap['xs'])
        self.ys = map(lambda y: round((y + 1) / 2 * h), beatmap['ys'])
        self.bmr = self._beatmap_reader()
        self.finished = False
        self.clock = time.Clock()
        self.c_x = 0 # current x position
        self.c_y = 0 # current y position
        self.c_beat = self.beats[0] # current beat in seconds
        self.buttons = [] # current buttons on screen
        self.counter = 0 # counter for button text
        self.time = -3
        self.error = 0.01
        self.score = 0
        self.combo = 0
        self.total_misses = 0
        self.failure_condition = 20
        self.circlehit = mixer.Sound('./assets/audio/circlehit.mp3')
        self.circlehit.set_volume(0.5)
        self.menuback = mixer.Sound('assets/audio/menuback.wav')

    def update(self):
        if not mixer.music.get_busy() and not self.finished:
            if (self.time >= -1):
                mixer.music.play()

        self.clock.tick()
        self.time += self.clock.get_rawtime() / 1000 # get time in seconds.
        self.time = round(self.time, 2)

        low = self.c_beat - self.error
        high = self.c_beat + self.error

        if self.time >= low and self.time <= high:
            try:
                self.c_beat, self.c_x, self.c_y = next(self.bmr)
            except StopIteration:
                self.finished = True
            if not self.finished:
                self._produce_beat(self.c_x, self.c_y)

        if self.finished:
            self.change_scene('title')

        for button in self.buttons:
            button.update()
        self.buttons = [button for button in self.buttons if button.visible]

    def render(self):
        self.surface.fill(self.color)
        for button in self.buttons:
            button.render()
        self.surface.blit(self.font.render(
            f'total: {self.score}', False, (0,0,0)),
            (1000, 20))
        self.surface.blit(self.font.render(
            f'{self.combo}x', False, (0,0,0)),
            (20, 1000))

    def handle_event(self, e):
        if e.type == events.COMBO_BREAK_EVENT:
            self.combo = 0
            self.total_misses += 1
            if self.total_misses >= self.failure_condition:
                self.score = 0
                self.total_misses += 1
                self.change_scene('map_select')
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                self.combo = 0
                self.score = 0
                self.total_misses = 0
                self.menuback.play()
                mixer.music.stop()
                self.change_scene('map_select')
            elif e.key == pg.K_r:
                self.restart()
            else:
                for button in self.buttons:
                    button.handle_event(e)


    def restart(self):
        for _ in self.bmr:
            pass
        self.bmr = self._beatmap_reader()
        self.buttons = []
        mixer.music.rewind()

    def _beatmap_reader(self):
        for b, x, y in zip(self.beats, self.xs, self.ys):
            yield b, x, y

    def _produce_beat(self, x, y):
        self.counter = (self.counter % 8) + 1
        w, h = self.img.get_size()
        button = CircleButton(str(self.counter), self.surface,
                        {'onclick': lambda x: self.hit(x)},
                        self.c_x - w // 2, self.c_y - h // 2,
                        w, h, None, img=self.img, font=self.font,
                        disappear_after=0.5)
        self.buttons.append(button)

    def hit(self, circle_button):
        self.circlehit.play()
        self.combo += 1
        self.score += 300 * self.combo
        circle_button.visible = False
        self.buttons = [button for button in self.buttons if button is not circle_button]



class CircleButton(Button):
    def __init__(self, text, surface, action, x, y, w, h, colors,
                 img=None, font=None, movable=True, disappear_after=0):
        super().__init__(text, surface, action, x, y, w, h, colors,
            img=img, font=font, movable=movable)
        self.disappear_after = disappear_after
        self.clock = time.Clock()
        self.time = 0
        self.visible = True
        self.center = (self.x + self.w/2, self.y + self.h/2)
        self.c_radius = self.w

    def update(self):
        self.clock.tick()
        self.time += self.clock.get_rawtime() / 1000 # get time in seconds.
        self.time = round(self.time, 2)
        if self.time >= self.disappear_after:
            self.visible = False
            combo_break_event = pg.event.Event(events.COMBO_BREAK_EVENT)
            pg.event.post(combo_break_event)
        else:
            self.visible = True

    def render(self):
        if self.visible:
            w, h = self.font.size(self.text)
            self.c_radius /= 1.004
            pg.draw.circle(self.surface, 0xffffff, self.center, self.c_radius, width=10)
            self.surface.blit(self.img, (self.x,self.y))
            self.surface.blit(self.font.render(
            self.text, False, (0,0,0)),
            self.center)

    def handle_event(self, e):
        if e.key == pg.K_z or pg.K_x:
            self.check_hovering()
            if self.hovering:
                self.action['onclick'](self)
