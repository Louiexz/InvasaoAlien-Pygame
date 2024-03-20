import sys
import os
import pygame as pyg
from alien import Alien
from bullet import Bullet

class GameFuncts:
    @staticmethod
    def new_text(screen, settings, txt, image=None):
        font = pyg.font.SysFont(None, 44)
        lines = txt[0].split("\n")
        text_surfaces = []
        for line_number, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (settings.screen_width * txt[1], settings.screen_height * 0.5 + line_number * 30)
            text_surfaces.append((text_surface, text_rect, txt[2]))
        returns = [text_surfaces]
        if image:
            image_surface = pyg.image.load(image)
            image_rect = image_surface.get_rect()
            image_rect.midbottom = (settings.screen_width * 0.53, settings.screen_height * 0.4)
            returns.append([image_surface, image_rect])
        GameFuncts.show_text(screen, *returns)

    @staticmethod
    def show_text(screen, text_surfaces, image=None):
        rects = []
        for text_surface, text_rect, time in text_surfaces:
            screen.blit(text_surface, text_rect)
            rects.append(text_rect)
        if image:
            screen.blit(image[0], image[1])
            rects.append(image[1])
        pyg.display.update(rects)
        pyg.time.delay(time)
    
    @staticmethod
    def play_sound(sound, tip=False):
        path = "sound/" + sound + ".mp3"
        if tip:
            if not pyg.mixer.music.get_busy():
                pyg.mixer.music.load(path)
                pyg.mixer.music.play()
        else: pyg.mixer.Sound(path).play()

    @staticmethod
    def shoot(character, bullets, settings):
        character.moving_left = character.moving_right = False
        if len(bullets) < settings.bullets_allowed:
            GameFuncts.play_sound("shoot")
            new_bullet = Bullet(settings, settings.screen, character)
            bullets.add(new_bullet)

    @staticmethod
    def show_settings(screen, settings):
        msg = """
    Alien Invasion (Invasão alienigena)\n
    - Quit ou tecla Esc para sair do jogo;\n
    - Stop/Rerun ou r: pause ou reinicia o jogo.\n
    - E para instruções;\n
    - Mover-se com: esquerda, direita ou cliques;\n
    - Mouse clique ou espaço para atirar;\n
    """
        text = [msg, 0.53, 3000]
        GameFuncts.new_text(screen, settings, text, './img/alien-male.png')

class GameControls:
    @staticmethod
    def reset_game(settings, aliens, bullets, character):
        settings.restart() # Reinicie as configurações e objetos do jogo   
        aliens.empty() # Remova todos os self.aliens e balas restantes
        bullets.empty()
        character.restart() # Reposicione a espaçonave

        settings.pause = False
        
    @staticmethod
    def handle_stop_restart(settings, bullets, aliens, character, pause=False):
        if pause: GameControls.reset_game(settings, aliens, bullets, character)
        else: pyg.time.delay(5000)
    
    @staticmethod
    def update_screen(screen, character, bullets, aliens, settings, buttons):
        if not settings.pause:
            screen.fill(settings.bg_color)
            character.blitme()
            aliens.draw(screen)
            updated_rects = []
            for alien in aliens.sprites(): updated_rects.append(alien.rect)
            for bullet in bullets.sprites(): bullet.draw_bullet()
            for button in buttons: button.draw(screen)
            msg = f"Bullets: {settings.bullets_allowed - len(bullets)}\nStage: {settings.stage}\nLifes: {settings.ship_lifes}"
            GameFuncts().new_text(screen, settings, [msg, 0.1, 10])
            # Crie uma lista de retângulos que precisam ser atualizados
            pyg.display.update(updated_rects)
    
    @staticmethod
    def game_over(screen, settings, bullets):
        GameFuncts().play_sound("game-over-transition", "music")
        GameFuncts().play_sound("game-over-voice")
        msg = f"Game Over\nUFO destroyed: {settings.count}\nStage: {settings.stage}"
        GameFuncts().new_text(screen, settings, [msg, 0.53, 10*5], './img/Alien-Reaching.png')
        while not settings.pause:
            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN and event.key == pyg.K_r:
                    GameControls().handle_stop_restart(settings, bullets, aliens, character)

    @staticmethod
    def render_game(screen, character, bullets, aliens, buttons, settings):
        screen.fill(settings.bg_color)
        character.blitme()
        aliens.draw(screen)

        for bullet in bullets.sprites(): bullet.draw_bullet()
        for button in buttons: button.draw(screen)

        pyg.display.flip()
    
    @staticmethod
    def control_frame_rate():
        clock = pyg.time.Clock()
        clock.tick(30)
    
    @staticmethod
    def main_game_loop(screen, character, bullets, aliens, settings, buttons):
        GameFuncts().show_settings(screen, settings)

        while settings.rodando:
            GameControls.update_screen(screen, character, bullets, aliens, settings, buttons)
            GameControls.render_game(screen, character, bullets, aliens, buttons, settings)
            GameControls.control_frame_rate()


class InputControls():
    @staticmethod
    def handle_keyboard_events(event, character, bullets, settings, aliens):
        if event.key == pyg.K_RIGHT: character.moving_right = True
        elif event.key == pyg.K_LEFT: character.moving_left = True
        elif event.key == pyg.K_SPACE: GameFuncts().shoot(character, bullets, settings)
        elif event.key == pyg.K_r: GameControls.handle_stop_restart(settings, bullets, aliens, character)

    @staticmethod
    def _process_mouse_input(event, character, settings, bullets):
        mouse_pos = pyg.mouse.get_pos()
        character.rect.centerx = character.center = mouse_pos[0]
        GameFuncts().shoot(character, bullets, settings)

    @staticmethod
    def handle_mouse_events(event, character, settings, bullets):
        if event.type == pyg.MOUSEBUTTONDOWN: InputControls._process_mouse_input(event, character, settings, bullets)
    
    @staticmethod
    def handle_input(screen, character, bullets, settings, aliens, buttons):
        for event in pyg.event.get():
            if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE): sys.exit()
            elif event.type == pyg.KEYDOWN: InputControls.handle_keyboard_events(event, character, bullets, settings, aliens)
            elif event.type == pyg.MOUSEBUTTONDOWN: InputControls.handle_mouse_events(event, character, settings, bullets)
            if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:  # Verifique se o clique foi com o botão esquerdo do mouse
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.text == "Stop/Rerun": GameControls.handle_stop_restart(settings, bullets, aliens, character)
                        elif button.text == "Instructions":
                            GameFuncts().play_sound("8bit-music", True)
                            GameFuncts().show_settings(screen, settings)
                        else: sys.exit()

class AliensFuncts:
    @staticmethod
    def nivels(settings):
        if settings.count % 100 == 0:
            settings.bullets_allowed += 2
            settings.ship_speed_factor += 5
            settings.alien_speed_factor += 5
            settings.bg_color = settings.espaco
        settings.stage += 1
        settings.alien_speed_factor += 2
        settings.bullet_speed_factor -= 1
        settings.ship_speed_factor += 1
        settings.bg_color = settings.ceu

    @staticmethod
    def aliens_killed(settings):
        GameFuncts().new_text(settings.screen, settings, ["UFO's count: " + str(settings.count), 0.8, 30])
        if settings.count % 20 == 0: AliensFuncts.nivels(settings)

    @staticmethod
    def check_bullet_alien_collisions(bullets, aliens, settings):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided
        collisions = pyg.sprite.groupcollide(bullets, aliens, True, True) 
        if collisions:
            for aliens in collisions.values():
                # each value is a list of aliens that were hit by the same bullet
                for alien in aliens:
                    alien.kill()
                    GameFuncts().play_sound("collision")
                    settings.count += 1
                    AliensFuncts.aliens_killed(settings)

    @staticmethod
    def change_fleet_direction(aliens, settings):
        # Faz toda a frota descer e muda sua direção.
        for alien in aliens.sprites(): alien.rect.y += settings.fleet_drop_speed
        settings.fleet_direction *= -1

    @staticmethod
    def check_fleet_edges(aliens, settings):
        for alien in aliens.sprites():
            if alien.check_edges():
                AliensFuncts.change_fleet_direction(aliens, settings)
                break

    @staticmethod
    def update_aliens(aliens, screen, bullets, settings):
        AliensFuncts.check_fleet_edges(aliens, settings)
        aliens.update()
        aliens.draw(screen)

    @staticmethod
    def handle_game_logic(screen, character, bullets, aliens, settings):
        AliensFuncts.update_aliens(aliens, screen, bullets, settings)
        AliensFuncts.check_bullet_alien_collisions(bullets, aliens, settings)
        AliensFuncts.check_aliens_bottom(screen, character, settings, aliens, bullets)

    @staticmethod
    def check_aliens_bottom(screen, character, settings, aliens, bullets):
        # Verifica se algum alienígena alcançou a parte inferior da tela.
        screen_rect = screen.get_rect()

        # Check for aliens hitting the bottom of the screen
        for alien in aliens.sprites():
            if alien.rect.bottom >= character.rect.top - 20:
                aliens.empty()
                settings.ship_lifes -= 1
                GameFuncts().play_sound("negative-beeps")
                if settings.ship_lifes < 1: GameControls().game_over(screen, settings, bullets)
    
    @staticmethod
    def get_random_aliens():
        # Gera um índice aleatório usando os.urandom
        archives = os.listdir('./img/aliens')
        random = int.from_bytes(os.urandom(4), byteorder='big') % len(archives)
    
        return archives[random]
    
    @staticmethod
    def create_alien(alien_width, alien_number, screen, settings, aliens, alien_image):
        """Create an alien and place it in the row."""
        alien = Alien(screen, settings, alien_image)
        alien_width = alien.rect.width
        alien.x = alien_width + 1.2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)

    @staticmethod
    def get_number_aliens_x(alien_width, settings):
        available_space_x = settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    @staticmethod
    def create_fleet(screen, settings, aliens, alien_image):
        alien = Alien(screen, settings, alien_image)
        alien_width = alien.rect.width
        number = AliensFuncts.get_number_aliens_x(alien_width, settings)

        for alien_number in range(number + 1): AliensFuncts.create_alien(alien_width, alien_number, screen, settings, aliens, alien_image)


class BulletFuncts:
    @staticmethod
    def update_bullets(bullets, aliens, settings):
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
                AliensFuncts().check_bullet_alien_collisions(bullets, aliens, settings)

class GameLoopManager:
    @staticmethod
    def run_game_loop(screen, character, bullets, settings, aliens, buttons):
        GameFuncts().show_settings(screen, settings)
        GameFuncts().play_sound("8bit-music", True)

        while settings.rodando:
            InputControls().handle_input(screen, character, bullets, settings, aliens, buttons)
            character.update()
            BulletFuncts().update_bullets(bullets, aliens, settings)
            AliensFuncts().handle_game_logic(screen, character, bullets, aliens, settings)

            if not aliens.sprites(): AliensFuncts().create_fleet(screen, settings, aliens, AliensFuncts().get_random_aliens())

            GameControls().update_screen(screen, character, bullets, aliens, settings, buttons)
            GameControls().render_game(screen, character, bullets, aliens, buttons, settings)
            GameControls().control_frame_rate()
