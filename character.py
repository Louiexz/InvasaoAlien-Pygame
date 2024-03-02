import pygame as pyg

class Character():
	def __init__(self, screen, photo, ai_sets=''):
		"""Inicializa a espaçonave e define sua posição inicial."""
		self.screen = screen
		self.sets = ai_sets
		# Carrega a imagem da espaçonave e obtém seu rect
		self.image = pyg.image.load(photo + '.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		# Inicia cada nova espaçonave na parte inferior central da tela
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		# Armazena um valor decimal para o centro da espaçonave
		self.center = float(self.rect.centerx)
		# Flags de movimento
		self.moving_right = False
		self.moving_left = False
	
	def blitme(self):
		"""Desenha a espaçonave em sua posição atual."""
		self.screen.blit(self.image, self.rect)
	
	def update(self):
		"""Atualiza a posição da espaçonave de acordo com as flags de movimento."""
		# Atualiza o valor do centro da espaçonave, e não o retângulo
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.moving_left = False
			self.center += self.sets.ship_speed_factor
		elif self.moving_left and self.rect.left > 0:
			self.moving_right = False
			self.center -= self.sets.ship_speed_factor
		self.rect.centerx = self.center

	def restart(self):
		self.rect.centerx = self.screen_rect.centerx

