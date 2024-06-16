import pygame as pyg
from pygame.sprite import Group

from ..character.ship import Ship
from .settings import Settings
from ..game.button import Button
from ..game.game_controls import GameControls

class InitializeGame:
    def __init__(self):
        pyg.init()
        pyg.display.set_caption("Alien Invasion")

        screen_info = pyg.display.Info()
        width = screen_info.current_w // 1.3
        height = screen_info.current_h // 1.3
        screen = pyg.display.set_mode((width, height))

        ai_sets = Settings(width, height, screen)
        ship = Ship(screen, ai_sets)
        buttons = [Button(pyg, *button) for button in ai_sets.buttons]

        bullets = Group()
        aliens = Group()

        GameControls.run_game_loop(screen, ship, bullets, ai_sets, aliens, buttons)
