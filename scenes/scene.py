# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 22:50:24 2020

@author: Christian Konstantinov
"""

import pygame as pg
from event import Event
from pygame import mixer

class Scene():
    def __init__(self, surface, color, font=None, bgi=None, bgm=None):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.font = font
        self.color = color
        self.bgi = bgi
        self.bgm = bgm

    def update(self):
        pass

    def render(self):
        pass

    def handle_event(self, e):
        pass

    def quit_game(self):
        pg.event.post(pg.event.Event(pg.QUIT))

    def change_scene(self, name):
        scene_change_event = pg.event.Event(Event.SCENE_CHANGE_EVENT,
                                            event_name=name)
        pg.event.post(scene_change_event)
    
class SceneManager():
    def __init__(self, scenes, current_scene, surface, cursor):
        self.scenes = scenes
        self.current_scene = current_scene
        self.surface = surface
        self.cursor = cursor

    def update(self):
        self.current_scene.update()

    def render(self):
        self.current_scene.render()
        self.render_cursor()

    def render_cursor(self):
        x, y = pg.mouse.get_pos()
        w, _ = self.cursor.get_size()
        self.surface.blit(self.cursor, (x - w // 2, y - w // 2))

class Button():
    def __init__(self, text, surface, action, x, y, w, h, colors,
                 img=None, font=None, movable=True, song=False):
        self.text = text
        self.surface = surface
        self.action = action
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h
        self.shape = pg.Rect(x, y, w, h)
        self.colors = colors
        self.state = 'idle'
        self.img = img
        self.font = font
        if not font:
            self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.movable = movable
        self.hovering = False
        self.dy = 0
        self.song = song
        self.menuhit = mixer.Sound('assets/audio/menuhit.wav')

    def update(self):
        self.check_hovering()
        self.y += self.dy
        self.shape.y += self.dy
        self.y2 = self.y + self.h
        if self.dy > 0:
            self.dy -= 5
        elif self.dy < 0:
            self.dy += 5

    def render(self):
        w, h = self.font.size(self.text)
        pg.Surface.fill(self.surface, self.colors[self.state], self.shape)
        self.surface.blit(self.font.render(
            self.text, False, (0,0,0)),
            (self.x + self.w/2 - w/2,self.y + self.h/2 - h/2))

    def handle_event(self, e):
        if e.type == pg.MOUSEBUTTONUP and e.button == 1:
            if self.hovering:
                self.menuhit.play()
                if not self.song:
                    self.action['onclick']()
                else:
                    self.action['onclick'](self.text)

    def check_hovering(self):
        x, y = pg.mouse.get_pos()
        if x >= self.x and x <= self.x2 and y >= self.y and y <= self.y2:
            self.hovering = True
            if pg.mouse.get_pressed()[0]:
                self.state = 'press'
            else:
                self.state = 'hover'
        else:
            self.hovering = False
            self.state = 'idle'
