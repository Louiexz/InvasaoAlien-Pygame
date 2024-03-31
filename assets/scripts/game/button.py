class Button:
    def __init__(self, pyg, *args):
        self.pyg = pyg
        self.rect = self.pyg.Rect(args[0:4])
        self.color = args[4]
        self.text = args[5]
        self.font = self.pyg.font.Font(None, 36)

    def draw(self, surface):
        self.pyg.draw.rect(surface, (150, 150, 150), self.rect)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
