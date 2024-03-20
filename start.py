import pygame as pyg
from pygame.sprite import Group
import character as characters
import settings as setts
from button import Button
from game_functions import GameLoopManager as loop

class InitializeGame:
    def __init__(self):
        pyg.init()
        pyg.display.set_caption("Alien Invasion")

        screen_info = pyg.display.Info()
        width = screen_info.current_w - 50
        height = screen_info.current_h - 50
        screen = pyg.display.set_mode((width, height))

        ai_sets = setts.Settings(width, height, screen)
        character = characters.Character(screen, 'img/new_ship2', ai_sets)
        buttons = [Button(pyg, *button) for button in ai_sets.buttons]

        bullets = Group()
        aliens = Group()

        loop.run_game_loop(screen, character, bullets, ai_sets, aliens, buttons)

if __name__ == "__main__": InitializeGame()