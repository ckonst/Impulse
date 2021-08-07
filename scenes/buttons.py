import pygame as pg
from pygame import mixer
from pygame import time

from abc import ABC

from events import Event

# TODO: state enum
class Button(ABC):

    def __init__(self, text, surface, onclick, x, y, w, h, colors,
                 img=None, font=None, movable=True, song=False):
        self.text = text
        self.surface = surface
        self.onclick = onclick
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
        if font is None:
            self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.movable = movable
        self.hovering = False
        self.dy = 0
        self.song = song
        self.sound = None
        

    def update(self):
        pass
    
    def render(self):
        pass

    def handle_event(self):
        pass

    def check_hovering(self):
        pass


class RectangleButton(Button):

    def __init__(self, text, surface, onclick, x, y, w, h, colors,
                 img=None, font=None, movable=True, is_song=False):
        super().__init__(text, surface, onclick, x, y, w, h, colors,
                         img=img, font=font, movable=movable)
        self.is_song = is_song
        self.sound = mixer.Sound('assets/audio/menuhit.wav')

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
            (self.x + self.w/2 - w/2, self.y + self.h/2 - h/2))

    def handle_event(self, e):
        if e.type == pg.MOUSEBUTTONUP and e.button == 1:
            if self.hovering:
                self.sound.play()
                if not self.is_song:
                    self.onclick()
                else: # pass the name through to play the map
                    self.onclick(self.text)

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

class CircleButton(Button):

    def __init__(self, text, surface, onclick, x, y, w, h, t, onset,
                 game_clock, colors=None, img=None, font=None,
                 movable=False, disappear_after=0, num=1):
        super().__init__(text, surface, onclick, x, y, w, h, colors,
                         img=img, font=font, movable=movable)
        self.sound = mixer.Sound('./assets/audio/circlehit.mp3')
        self.sound.set_volume(0.5)
        self.disappear_after = disappear_after
        self.clock = time.Clock()
        self.game_clock = game_clock
        self.time = t
        self.onset = onset
        self.tolerance = 0.3 # how far off the onset will we consider a click to be a hit
        self.visible = True
        self.center = (self.x + self.w/2, self.y + self.h/2)
        self.radius = w // 2
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
                    self.onclick(self)

    def check_hovering(self):
        x, y = pg.mouse.get_pos()
        xc, yc = self.center
        distance_squared = (x - xc)**2 + (y - yc)**2
        # if the distance squared is less than or equal to the radius,
        # then the point (mouse position) is on the circle.
        if distance_squared <= self.radius**2: 
            self.hovering = True
            if pg.mouse.get_pressed()[0]:
                self.state = 'press'
            else:
                self.state = 'hover'
        else:
            self.hovering = False
            self.state = 'idle'