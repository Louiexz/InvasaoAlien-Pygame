import sys
import os
import pygame as pyg
from alien import Alien
from bullet import Bullet
from button import Button

archives = os.listdir('./img/aliens')
GAME_SPEED = 30
updated_rects = []

def get_aliens():
    # Gera um índice aleatório usando os.urandom
    random = int.from_bytes(os.urandom(4), byteorder='big') % len(archives)
    
    return archives[random]

def new_text(settings, txt, image=None):
    font = pyg.font.SysFont(None, 44)
    lines = txt[0].split("\n")
    text_surfaces = []
    for line_number, line in enumerate(lines):
        text_surface = font.render(line, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (settings.screen_width * txt[1], settings.screen_height * 0.5 + line_number * 30)
        text_surfaces.append((text_surface, text_rect, txt[2]))
    returns = [settings, text_surfaces]
    if image:
        image_surface = pyg.image.load(image)
        image_rect = image_surface.get_rect()
        image_rect.midbottom = (settings.screen_width * 0.53, settings.screen_height * 0.4)
        returns.append([image_surface, image_rect])
    show_text(*returns)

def show_text(settings, text_surfaces, image=None):
    rects = []
    for text_surface, text_rect, time in text_surfaces:
        settings.screen.blit(text_surface, text_rect)
        rects.append(text_rect)
    if image:
        settings.screen.blit(image[0], image[1])
        rects.append(image[1])
    pyg.display.update(rects)
    pyg.time.delay(time)

def nivels(sets):
    if sets.count % 100 == 0:
        sets.bullets_allowed += 2
        sets.ship_speed_factor += 5
        sets.alien_speed_factor += 5
        sets.fleet_drop_speed += 10
        sets.bg_color = sets.espaco
    sets.alien_speed_factor += 2
    sets.bullet_speed_factor -= 1
    sets.ship_speed_factor -= 1
    sets.bg_color = sets.ceu

def aliens_killed(sets):
	text = ["UFO's count: " + str(sets.count), 0.8, 10]
	new_text(sets, text)

	if sets.count % 20 == 0: nivels(sets)

def play_sound(sound):
    som = pyg.mixer.Sound("sound/" + sound + ".mp3")

    som.play()

def check_bullet_alien_collisions(aliens, bullets, sets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided
    collisions = pyg.sprite.groupcollide(bullets, aliens, True, True) 
    if collisions:
        for aliens in collisions.values():
            # each value is a list of aliens that were hit by the same bullet
            for alien in aliens:
                alien.kill()
                play_sound("collision")
                sets.count += 1
                aliens_killed(sets)

def update_bullets(sets, screen, character, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
    	if bullet.rect.bottom <= 0:
    	    bullets.remove(bullet)
    	    updated_rects.append(bullet.rect)
    check_bullet_alien_collisions(aliens, bullets, sets)

def change_fleet_direction(sets, aliens):
	# Faz toda a frota descer e muda sua direção.
	for alien in aliens.sprites(): alien.rect.y += sets.fleet_drop_speed
	sets.fleet_direction *= -1

def check_fleet_edges(sets, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(sets, aliens)
            break

def update_aliens(sets, screen, aliens, bullets):
    check_fleet_edges(sets, aliens)
    aliens.update()
    aliens.draw(screen)

def game_over(character, bullets, sets, screen, aliens):
    new_text(sets, ["Game Over\nUFO destroyed:" + str(sets.count), 0.53, 10*5], './img/Alien-Reaching.png')
    
    while sets.rodando == True:
        pyg.image.load('./img/Alien-Reaching.png')
        for event in pyg.event.get():
            if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE): sys.exit()
            elif event.type == pyg.KEYDOWN and event.key == pyg.K_r:
                sets.rodando == False
                handle_stop_restart(sets, character, bullets, screen, aliens, True)
	
def check_aliens_bottom(character, bullets, sets, screen, aliens):
    # Verifica se algum alienígena alcançou a parte inferior da tela.
    screen_rect = screen.get_rect()
    
    # Check for aliens hitting the bottom of the screen
    for alien in aliens.sprites():
        if alien.rect.bottom >= character.rect.top - 20:
            # Treat this the same as if the character got hit.
            sets.rodando = False
            game_over(character, bullets, sets, screen, aliens)

def handle_game_logic(character, bullets, sets, screen, aliens):
    update_bullets(sets, screen, character, aliens, bullets)
    update_aliens(sets, screen, aliens, bullets)
    check_aliens_bottom(character, bullets, sets, screen, aliens)

def shoot(character, bullets, sets, screen):
    character.moving_left = character.moving_right = False
    if len(bullets) < sets.bullets_allowed:
        play_sound("shoot")
        new_bullet = Bullet(sets, screen, character)
        bullets.add(new_bullet)

def handle_keyboard_events(event, character, bullets, sets, screen, aliens):
    if event.key == pyg.K_RIGHT: character.moving_right = True
    elif event.key == pyg.K_LEFT: character.moving_left = True
    elif event.key == pyg.K_SPACE: shoot(character, bullets, sets, screen)
    elif event.key == pyg.K_r: handle_stop_restart(sets, character, bullets, screen, aliens)

def _process_mouse_input(event, character, sets, bullets, aliens):
	mouse_pos = pyg.mouse.get_pos()
	character.rect.centerx = character.center = mouse_pos[0]
	shoot(character, bullets, sets, sets.screen)

def handle_mouse_events(event, character, sets, bullets, aliens):
    if event.type == pyg.MOUSEBUTTONDOWN: _process_mouse_input(event, character, sets, bullets, aliens)

def show_sets(sets):
	msg = """
Alien Invasion (Invasão alienigena)\n\n
- Quit ou tecla Esc para sair do jogo;\n
- Stop/Rerun ou r: pause ou reinicia o jogo.\n
- E para instruções;\n
- Mover-se com: esquerda, direita ou cliques;\n
- Mouse clique ou espaço para atirar;\n
"""
	text = [msg, 0.53, 3000]
	new_text(sets, text, './img/alien-male.png')

def handle_input(screen, character, bullets, sets, aliens, buttons):
    for event in pyg.event.get():
        if event.type == pyg.QUIT or (event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE): sys.exit()
        elif event.type == pyg.KEYDOWN: handle_keyboard_events(event, character, bullets, sets, screen, aliens)
        elif event.type == pyg.MOUSEBUTTONDOWN:
        	handle_mouse_events(event, character, sets, bullets, aliens)
        	if event.button == 1:  # Verifique se o clique foi com o botão esquerdo do mouse
        		for button in buttons:
        			if button.rect.collidepoint(event.pos):
        				if button.text == "Stop/Rerun": handle_stop_restart(sets, character, bullets, screen, aliens)
        				elif button.text == "Instructions": show_sets(sets)
        				else: sys.exit()

def reset_game(character, bullets, aliens, sets, screen):
    sets.restart() # Reinicie as configurações e objetos do jogo   
    aliens.empty() # Remova todos os aliens e balas restantes
    bullets.empty()
    character.restart() # Reposicione a espaçonave
    
    game_loop(aliens, bullets, character, sets, screen)

def handle_stop_restart(sets, character, bullets, screen, aliens, stop_restart=False):
    if stop_restart: reset_game(character, bullets, aliens, sets, screen)
    else: pyg.time.delay(10000)

def update_screen(screen, character, bullets=None, sets=None, aliens=None, buttons=None):
    screen.fill(sets.bg_color)
    character.blitme()
    aliens.draw(screen)
    for alien in aliens.sprites(): updated_rects.append(alien.rect)
    for bullet in bullets.sprites(): bullet.draw_bullet()
    for button in buttons: button.draw(screen)
    new_text(sets, ["Bullets: " + str(3 - len(bullets)), 0.1, 1])
    # Crie uma lista de retângulos que precisam ser atualizados
    pyg.display.update(updated_rects)

def create_alien(aliens, sets, alien_number, alien_image):
    """Create an alien and place it in the row."""
    alien = Alien(sets.screen, sets, alien_image)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.2 * alien_width * alien_number
    alien.rect.x = alien.x
    aliens.add(alien)

def get_number_aliens_x(sets, alien_width):
    available_space_x = sets.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_fleet(sets, screen, aliens, alien_image):
    alien = Alien(screen, sets, alien_image)
    alien_width = alien.rect.width
    number = get_number_aliens_x(sets, alien_width)
    
    for alien_number in range(number + 1): create_alien(aliens, sets, alien_number, alien_image)

def game_loop(aliens, bullets, character, sets, screen):
	buttons = [Button(pyg, *button) for button in sets.buttons]
	show_sets(sets)
	while sets.rodando:
		global updated_rects
		updated_rects = []

		if not aliens.sprites():
		    alien_image = get_aliens()
		    create_fleet(sets, screen, aliens, alien_image)

		for x in [character, bullets, aliens]: x.update()
		handle_input(screen, character, bullets, sets, aliens, buttons)
		handle_game_logic(character, bullets, sets, screen, aliens)
		update_screen(screen, character, bullets, sets, aliens, buttons)

		# Optionally, add a delay to control the game loop speed
		clock = pyg.time.Clock()
		clock.tick(GAME_SPEED)
		pyg.display.flip()
