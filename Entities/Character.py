import pygame
import os


def get_dir_images(number, width):
    images = {}
    for img in os.listdir(fr'Assets\Characters\{number}'):
        name, nb = img.split('_')[0].lower(), int(img.split('_')[-1][:-4])
        if name not in images:
            images[name] = []
        image = pygame.image.load(fr'Assets\Characters\{number}\{img}')
        rat = image.get_width()/image.get_height()
        image = pygame.transform.scale(image, (width, width/rat)).convert_alpha()
        images[name].insert(nb, image)
    return images


class Character(pygame.sprite.Sprite):
    vertical_speed = 2

    def __init__(self, number: int, width):
        super().__init__()
        self.images = get_dir_images(number, width)
        self.animating = False
        self.showing = False
        self.state = 'idle'
        self.animating_step = 0
        self.image = pygame.Surface((0, 0))
        self.rect: pygame.Rect = self.images['idle'][0].get_rect()

    def animate(self):
        if self.animating:
            images = self.images[self.state]
            self.image = images[self.animating_step]
            self.animating_step = 0 if len(images) == self.animating_step else self.animating_step + 1

    def change_pos(self, pos: tuple[int, int]):
        self.rect.x, self.rect.y = pos

    def change_state(self, state):
        self.state = state
        self.animating_step = 0

    def update(self):
        pass
