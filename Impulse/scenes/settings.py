import pygame as pg
from buttons import RectangleButton
from pygame import mixer
from scene import Scene


class Settings(Scene):

    def __init__(self, surface, color, font=None, bgi=None, bgm=None):
        super().__init__(surface, color, font=font, bgi=bgi, bgm=bgm)

    def update(self):
        pass

    def render(self):
        self.surface.fill(self.color)
        self.surface.blit(self.font.render('Settings', False, (0, 0, 0)),
                          (self.width / 2, self.height / 6))

    def handle_event(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            self.menuback.play()
            self.change_scene('title')
