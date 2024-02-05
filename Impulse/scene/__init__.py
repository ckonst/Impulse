from abc import ABC, abstractmethod

import pygame as pg
from pygame import mixer
from Impulse.events import Event


class Scene(ABC):

    def __init__(self, surface, color, font=None, bgi=None, bgm=None):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.font = font
        self.color = color
        self.bgi = bgi
        self.bgm = bgm
        self.menuback = mixer.Sound('./Impulse/data/assets/audio/menuback.wav')

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handle_event(self, e):
        pass

    def quit_game(self):
        pg.event.post(pg.event.Event(pg.QUIT))

    def change_scene(self, name):
        scene_change_event = pg.event.Event(Event.SCENE_CHANGE_EVENT, event_name=name)
        pg.event.post(scene_change_event)


class SceneManager:

    def __init__(self, scenes, current_scene, surface, cursor, clock):
        self.scenes = scenes
        self.current_scene = current_scene
        self.surface = surface
        self.cursor = cursor
        self.clock = clock

    def update(self):
        self.current_scene.update()

    def render(self):
        self.current_scene.render()
        self._render_cursor()
        self._render_fps_meter()

    def handle_events(self, beat_manager) -> bool:
        running = True
        for e in pg.event.get():
            match (e.type):
                case pg.QUIT:
                    running = False
                case Event.BEATMAP_UPDATE_EVENT:
                    self.scenes.update(beat_manager.beatmaps)
                case Event.SCENE_CHANGE_EVENT:
                    self.current_scene = self.scenes[e.event_name]
                case _:
                    pass
            self.current_scene.handle_event(e)
        return running

    def _render_cursor(self):
        x, y = pg.mouse.get_pos()
        w, _ = self.cursor.get_size()
        self.surface.blit(self.cursor, (x - w // 2, y - w // 2))

    def _render_fps_meter(self):
        self.surface.blit(
            self.current_scene.font.render(f'fps: {int(self.clock.get_fps())}', False, (0, 0, 0)),
            (self.current_scene.width - 200, 20),
        )
