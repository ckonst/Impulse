# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 22:50:24 2020

@author: Christian Konstantinov
"""

import pygame as pg
import events

class Scene():
    def __init__(self, window, running=True, font=None, bgi=None, bgm=None):
        self.window = window
        self.running = running
        self.font = font
        self.bgi = bgi
        self.bgm = bgm
    def update(self):
        pass
    def render(self):
        pass
    def handle_event():
        pass
    def to_map_select(self):
        self.change_scene('map_select')
    def to_settings(self):
        self.change_scene('settings')
    def to_title(self):
        self.change_scene('title')
    def quit_game(self):
        pg.event.post(pg.QUIT)
    def change_scene(self, name):
        scene_change_event = pg.event.Event(events.SCENE_CHANGE_EVENT,
                                            event_name=name)
        pg.event.post(scene_change_event)

class SceneManager():
    def __init__(self, scenes, current_scene):
        self.scenes = scenes
        self.current_scene = current_scene
    def update(self):
        self.current_scene.update()
    def render(self):
        self.current_scene.render()
