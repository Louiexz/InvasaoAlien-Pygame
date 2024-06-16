import os
import pygame as pyg
from .alien import Alien

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
        settings.ship_speed_factor += 1
        if settings.bg_color != settings.espaco: settings.bg_color = settings.ceu

    @staticmethod
    def aliens_killed(settings):
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
                    settings.count += 1
                    AliensFuncts.aliens_killed(settings)
                    return True
        return False

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
    def update_aliens(aliens, screen, settings):
        AliensFuncts.check_fleet_edges(aliens, settings)
        aliens.update()
        aliens.draw(screen)
    
    @staticmethod
    def check_aliens_bottom(screen, ship, settings, aliens):
        # Verifica se algum alienígena alcançou a parte inferior da tela.
        screen_rect = screen.get_rect()

        # Check for aliens hitting the bottom of the screen
        for alien in aliens.sprites():
            if alien.rect.bottom >= ship.rect.top - 20:
                aliens.empty()
                settings.ship_lifes -= 1
                if settings.ship_lifes < 1:
                    settings.rodando = False
                    return True
        return False

    @staticmethod
    def handle_game_logic(screen, ship, bullets, aliens, settings):
        logica = []
        AliensFuncts.update_aliens(aliens, screen, settings)
        logica.append(AliensFuncts.check_bullet_alien_collisions(bullets, aliens, settings))
        logica.append(AliensFuncts.check_aliens_bottom(screen, ship, settings, aliens))
        return logica
    
    @staticmethod
    def get_random_aliens():
        # Gera um índice aleatório usando os.urandom
        archives = os.listdir('./assets/imagens/enemies/aliens')
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

        for alien_number in range(number + 1):
            AliensFuncts.create_alien(alien_width, alien_number, screen, settings, aliens, alien_image)
