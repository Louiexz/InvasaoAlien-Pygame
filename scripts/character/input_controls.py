import sys
import pygame as pyg

class InputControls():
    @staticmethod
    def handle_keyboard_events(event, ship):
        if event.key == (pyg.K_RIGHT or pyg.K_d): ship.moving_right = True
        elif event.key == (pyg.K_LEFT or pyg.K_a): ship.moving_left = True
        elif event.key == pyg.K_SPACE: return 1
        elif event.key == pyg.K_r: return 2
        elif event.key == pyg.K_e: return 3
    
    @staticmethod
    def _process_mouse_input(event, ship, buttons):
        if event.button == 1:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Stop/Rerun": return 2
                    elif button.text == "Instructions": return 3
                    else: sys.exit()
        
        mouse_pos = pyg.mouse.get_pos()
        ship.rect.centerx = ship.center = mouse_pos[0]
        return 1

    @staticmethod
    def handle_input(ship, buttons):
        for event in pyg.event.get():
            if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE): sys.exit()
            elif event.type == pyg.KEYDOWN: return InputControls.handle_keyboard_events(event, ship)
            elif event.type == pyg.MOUSEBUTTONDOWN: return InputControls._process_mouse_input(event, ship, buttons)
            