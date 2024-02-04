import pygame as pg
from events import Event
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
        self.menuback = mixer.Sound('assets/audio/menuback.wav')

    def update(self):
        pass

    def render(self):
        pass

    def handle_event(self, e):
        pass

    def quit_game(self):
        pg.event.post(pg.event.Event(pg.QUIT))

    def change_scene(self, name):
        scene_change_event = pg.event.Event(Event.SCENE_CHANGE_EVENT, event_name=name)
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
        self._render_cursor()

    def _render_cursor(self):
        x, y = pg.mouse.get_pos()
        w, _ = self.cursor.get_size()
        self.surface.blit(self.cursor, (x - w // 2, y - w // 2))
