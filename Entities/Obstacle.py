import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, name, image: pygame.Surface, size, active=True, matrix=None):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.name = name
        self.x, self.y = 0, 0
        self.size = size
        if active:
            if matrix is None:
                matrix = [[1 for c in range(size[1])] for m in range(size[1])]
        else:
            matrix = [[0 for c in range(size[1])] for m in range(size[1])]
        self.matrix = matrix

    def set_pos(self, pos):
        self.rect.x, self.rect.y = pos

    def set_row_column(self, pos):
        self.x, self.y = pos
