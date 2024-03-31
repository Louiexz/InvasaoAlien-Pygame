import pygame as pyg
from scripts.character.bullet import Bullet

class GameFuncts:
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
    def new_text(screen, settings, txt, image=None):
        font = pyg.font.SysFont(None, 38)
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
    def play_sound(sound, tip=False):
        path = "./sound/" + sound + ".mp3"
        if tip:
            if not pyg.mixer.music.get_busy():
                pyg.mixer.music.load(path)
                pyg.mixer.music.play()
        else: pyg.mixer.Sound(path).play()

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
        text = [msg, 0.53, 4000]
        GameFuncts.play_sound("game/8bit-music", True)
        GameFuncts.new_text(screen, settings, text, './assets/enemies/alien-male.png')

    @staticmethod
    def shoot(ship, bullets, settings):
        ship.moving_left = ship.moving_right = False
        if len(bullets) < settings.bullets_allowed:
            new_bullet = Bullet(settings, settings.screen, ship)
            bullets.add(new_bullet)
            GameFuncts.play_sound("ship/shoot")
