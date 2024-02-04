import pygame as pg
from buttons import RectangleButton
from pygame import mixer
from scene import Scene


class Title(Scene):

    def __init__(self, surface, color, font=None, bgi=None, bgm=None):
        super().__init__(surface, color, font, bgi, bgm)
        self.colors = {
            'idle': (0xA0, 0xB6, 0xBD),
            'hover': (0x8E, 0xBA, 0xC8),
            'press': (0x79, 0x8A, 0x8F),
        }
        w = 600
        h = 100
        x = self.width // 2 - w // 2
        y = self.height // 2 - h // 1.5
        self.menu_items = [
            RectangleButton(
                'Play',
                self.surface,
                lambda: self.change_scene('map_select'),
                x,
                y,
                w,
                h,
                self.colors,
                font=font,
            ),
            RectangleButton(
                'Settings',
                self.surface,
                lambda: self.change_scene('settings'),
                x,
                y + 150,
                w,
                h,
                self.colors,
                font=font,
            ),
            RectangleButton(
                'Quit',
                self.surface,
                self.quit_game,
                x,
                y + 300,
                w,
                h,
                self.colors,
                font=font,
            )
        ]
        self.title_img = pg.image.load('assets/img/title.png')
        self.logo_img = pg.image.load('assets/img/waveform.png')

    def update(self):
        for button in self.menu_items:
            button.update()

    def render(self):
        self.surface.fill(self.color)
        self.surface.blit(self.title_img, (self.width // 2.75, self.height // 9.5))
        self.surface.blit(self.logo_img, (self.width // 2.75 - 20, 60))
        for button in self.menu_items:
            button.render()

    def handle_event(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            self.quit_game()
        else:
            for button in self.menu_items:
                button.handle_event(e)
