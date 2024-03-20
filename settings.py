class Settings():
	"""Uma classe para armazenar todas as configurações da Invasão
	Alienígena."""
	def __init__(self, screen_width, screen_height, screen):
		# Configurações da tela
		self.screen = screen
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.bg_color = (100, 100, 100)
		self.espaco = (0, 0, 33)
		self.ceu= (135, 206, 235)
		# Levels
		self.stage = 0
		# Configurações dos projéteis
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullet_speed_factor = 15
		self.bullets_allowed = 3
		# Configurações da espaçonave
		self.ship_speed_factor = 3
		self.ship_lifes = 5
		# Configurações dos alienígenas
		self.alien_speed_factor = 5
		self.fleet_drop_speed = 50
		# fleet_direction igual a 1 representa direita; -1 representa a esquerda
		self.fleet_direction = 1
		# Aliens mortos
		self.count = 0
		# Botões
		button1_rect = [screen_width * 0.75, screen_height * 0.05, 160, 40, (0, 0, 0), "Instructions"]
		button2_rect = [20, screen_height * 0.2, 140, 40, (255, 0, 0), "Quit"]
		button3_rect = [20, screen_height * 0.25, 140, 40, (0, 0, 0), "Stop/Rerun"]

		self.buttons = [button1_rect, button2_rect, button3_rect]

		# Loop
		self.pause = False
		self.rodando = True

	def restart():
		self.alien_speed_factor = 1
		self.bullets_allowed = 3
		self.bg_color = True
		self.fleet_drop_speed = 40
		self.ship_speed_factor = 5