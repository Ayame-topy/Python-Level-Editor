import pygame
from Game import Game


class App:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = self.init_screen()
        self.game = Game(self.screen)
        self.game.init()

    def init_screen(self):
        sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Level Maker')
        return sc

    def main_loop(self):
        while self.game.running:
            self.game.update()
            pygame.display.flip()
