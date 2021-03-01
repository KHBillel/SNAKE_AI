import pygame

class Block :
    def __init__(self, x, y,color) :
        self.surface = pygame.Surface((10, 10))
        self.surface.fill(color)
        self.rect = self.surface.get_rect()
        self.rect.center=(x,y)