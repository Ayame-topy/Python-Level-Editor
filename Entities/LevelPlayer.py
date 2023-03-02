import pygame


class LevelPlayer:
    def __init__(self, screen):
        self.player = None
        self.level = None
        self.screen = screen

    def set_player(self, player):
        self.player = player

    def set_level(self, level):
        self.level = level
