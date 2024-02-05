import logging as log
from functools import wraps

import pygame as pg

from Impulse.beatmap import BeatMapManager
from Impulse.events import Event
from Impulse.scene import SceneManager
from Impulse.scene.map import Map
from Impulse.scene.map_select import MapSelect
from Impulse.scene.settings import Settings
from Impulse.scene.title import Title


def pygame_app(f):
    log.basicConfig(level=log.DEBUG)

    @wraps(f)
    def wrapper(*args, **kwargs):
        pg.init()
        try:
            f(*args, **kwargs)
        except Exception as ex:
            log.exception(ex)
        finally:
            log.info('Exiting.')
            pg.quit()

    return wrapper


@pygame_app
def main():
    # display stuff
    info = pg.display.Info()
    surface = pg.display.set_mode((info.current_w, info.current_h))
    surface.convert()
    bg_color = 0x464f53
    cursor = pg.image.load('./Impulse/data/assets/img/cursor.png')
    pg.mouse.set_visible(False)

    FONT_PATH = './Impulse/data/assets/fonts/Gidole-Regular.otf'
    font = pg.font.Font(FONT_PATH, 48)
    clock = pg.time.Clock()
    beat_manager = BeatMapManager(clock, surface, bg_color, font)

    scenes: dict[str, Map] = {
        'title': Title(surface, bg_color, font=font),
        'settings': Settings(surface, bg_color, font=font),
        'map_select': MapSelect(surface, bg_color, beat_manager, font=font),
        **beat_manager.beatmaps
    }

    scene_manager = SceneManager(scenes, scenes['title'], surface, cursor, clock)

    running = True

    while running:
        running = scene_manager.handle_events(beat_manager)
        scene_manager.update()
        scene_manager.render()
        pg.display.update()
        clock.tick()
