import pygame as pyg
from pygame.sprite import Group
import character as characters
import settings as sets
import game_functions as g_f

def initialize_game():
	# Inicializa o jogo e cria um objeto para a tela
	pyg.init()
	pyg.display.set_caption("Alien Invasion")
	# Obtém a resolução da tela do dispositivo
	screen_info = pyg.display.Info()
	# Cria a tela com base na resolução do dispositivo
	width = screen_info.current_w - 50
	height = screen_info.current_h - 50
	screen = pyg.display.set_mode((width, height))
	ai_sets = sets.Settings(width, height, screen)
	# Cria uma espaçonave
	character = characters.Character(screen, 'img/new_ship2', ai_sets)
	# Cria um grupo no qual serão armazernados os projéteis e aliens
	bullets = Group()
	# Cria um alienígena
	aliens = Group()
	# Inicia o laço principal do jogo
	g_f.game_loop(aliens, bullets, character, ai_sets, screen)

initialize_game()
