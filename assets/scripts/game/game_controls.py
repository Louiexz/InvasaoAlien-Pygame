import sys
import pygame as pyg
from ..character.input_controls import InputControls
from ..enemies.aliens_functs import AliensFuncts
from .game_functs import GameFuncts

class GameControls:
    @staticmethod
    def update_bullets(bullets, aliens, settings):
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
                update = AliensFuncts.check_bullet_alien_collisions(bullets, aliens, settings)
                try:
                    if len(update) == 2:
                        GameFuncts.play_sound(update[0])
                        GameFuncts.game_over(update[1])
                except Exception as e: pass

    @staticmethod
    def reset_game(settings, aliens, bullets, ship):
        bullets.empty()
        aliens.empty() # Remova todos os self.aliens e balas restantes
        ship.restart() # Reposicione a espaçonave
        settings.restart() # Reinicie as configurações e objetos do jogo   

        settings.pause = False
    
    @staticmethod
    def handle_stop_restart(settings, bullets, aliens, ship, pause=False):
        if pause: GameControls.reset_game(settings, aliens, bullets, ship)
    
    @staticmethod
    def render_game(screen, ship, bullets, aliens, buttons, settings):
        screen.fill(settings.bg_color)
        ship.blitme()
        aliens.draw(screen)

        for bullet in bullets.sprites(): bullet.draw_bullet()
        for button in buttons: button.draw(screen)

        pyg.display.flip()

    @staticmethod
    def control_frame_rate():
        clock = pyg.time.Clock()
        clock.tick(60)
    
    @staticmethod
    def update_screen(screen, ship, bullets, aliens, settings, buttons):
        if not settings.pause:
            screen.fill(settings.bg_color)
            ship.blitme()
            aliens.draw(screen)
            updated_rects = []
            for alien in aliens.sprites(): updated_rects.append(alien.rect)
            for bullet in bullets.sprites(): bullet.draw_bullet()
            for button in buttons: button.draw(screen)
            msg = f'''
Bullets: {settings.bullets_allowed - len(bullets)}
Stage: {settings.stage}\nLifes: {settings.ship_lifes}
UFO's count: {settings.count}'''
            GameFuncts.new_text(screen, settings, [msg, 0.1, 10])
            # Crie uma lista de retângulos que precisam ser atualizados
            pyg.display.update(updated_rects)
    
    @staticmethod
    def main_game_loop(screen, ship, bullets, aliens, settings, buttons):
        GameFuncts.show_settings(screen, settings)

        while settings.rodando:
            GameControls.update_screen(screen, ship, bullets, aliens, settings, buttons)
            GameControls.render_game(screen, ship, bullets, aliens, buttons, settings)
            GameControls.control_frame_rate()
    
    @staticmethod
    def game_over(screen, settings, bullets, aliens, ship, buttons):
        GameFuncts.play_sound("game/game-over-transition", True)
        GameFuncts.play_sound("game/game-over-voice")
        msg = f"Game Over\nUFO destroyed: {settings.count}\nStage: {settings.stage}"
        GameFuncts.new_text(screen, settings, [msg, 0.53, 10*5], './assets/imagens/enemies/alien-reaching.png')
        while not settings.rodando:
            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN and event.key == pyg.K_r:
                    GameControls.handle_stop_restart(settings, bullets, aliens, ship, True)
                    settings.rodando = True
                elif event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE): sys.exit()
                # Verifique se o clique foi com o botão esquerdo do mouse
                if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.text == "Stop/Rerun":
                                GameControls.handle_stop_restart(settings, bullets, aliens, ship, True)
                                settings.rodando = True
                            else: sys.exit()
    
    @staticmethod
    def run_game_loop(screen, ship, bullets, settings, aliens, buttons):
        GameFuncts.play_sound("game/8bit-music", True)
        GameFuncts.show_settings(screen, settings)
        while True:
            input = InputControls().handle_input(ship, buttons)
            if input == 1: GameFuncts.shoot(ship, bullets, settings)
            elif input == 2:
                GameFuncts.new_text(screen, settings, ["Jogo pausado", 0.53, 10000])
                GameControls.handle_stop_restart(settings, bullets, aliens, ship)
            elif input == 3:
                GameFuncts.play_sound("game/8bit-music")
                GameFuncts.show_settings(screen, settings)
            
            ship.update()
            GameControls().update_bullets(bullets, aliens, settings)
            
            som = AliensFuncts().handle_game_logic(screen, ship, bullets, aliens, settings)
            if som[0]: GameFuncts().play_sound("aliens/collision")
            elif som[1]:
                GameFuncts().play_sound("game/negative-beeps")
                GameControls().game_over(screen, settings, bullets, aliens, ship, buttons)

            if not aliens.sprites(): AliensFuncts().create_fleet(screen, settings, aliens, AliensFuncts().get_random_aliens())

            GameControls().update_screen(screen, ship, bullets, aliens, settings, buttons)
            GameControls().render_game(screen, ship, bullets, aliens, buttons, settings)
            GameControls().control_frame_rate()
