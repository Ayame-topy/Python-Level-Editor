import tkinter.filedialog

import pygame
import json
from tkinter.filedialog import *


class Level:
    def __init__(self, size, from_file=False):
        self.group = pygame.sprite.Group()
        self.obstacles = {}
        self.matrix = []
        self.size = size
        self.init_matrix()
        if from_file:
            try:
                self.load_from_file()
                self.loaded = True
            except Exception as ex:
                self.loaded = False
                print(ex)

    def init_matrix(self):
        x, y = self.size
        self.matrix = [[0 for i in range(x)] for i in range(y)]

    def load_from_file(self):
        file = askopenfile(filetypes=(('Json', '*.json'), ))
        if file is not None:
            data = json.load(file)
            matrix = data['matrix']
            self.blocks_nb = wd, height = [int(i) for i in data['size']]
            if [len(column) for column in matrix] == [wd]*height:
                self.matrix = matrix
            else:
                raise ValueError

    def add_obstacle(self, obstacle):
        self.group.add(obstacle)
        name = obstacle.name
        if name not in self.obstacles:
            self.obstacles[name] = []
        self.obstacles[name].append((obstacle.x, obstacle.y))
        self.refresh_matrix()

    def extend_size(self, side):
        self.blocks_nb = self.blocks_nb[0]+side, self.blocks_nb[1]
        if side == 1:
            for c in self.matrix:
                c.append(0)

        else:
            for c in self.matrix:
                c.pop(-1)

    def save_as_file(self):
        to_dump = {'size': self.blocks_nb, 'matrix': self.matrix}
        file = asksaveasfile(initialfile='Level.json', filetypes=(('Json', '*.json'), ))
        if file is not None:
            json.dump(to_dump, file)

    def clear_block(self, pos):
        for obstacle in self.group:
            x, y = obstacle.x, obstacle.y
            if x <= pos[0] <= x + obstacle.size[0]-1 and y <= pos[1] <= y + obstacle.size[1]-1:
                self.remove_obstacle(obstacle)

    def remove_obstacle(self, obstacle):
        if obstacle not in self.group: exit(obstacle)
        self.group.remove(obstacle)
        self.obstacles[obstacle.name].remove((obstacle.x, obstacle.y))

    def refresh_matrix(self):
        self.init_matrix()
        for obstacle in self.group:
            for y in range(obstacle.size[1]):
                for x in range(obstacle.size[0]):
                    self.matrix[y + obstacle.y][x + obstacle.x] = obstacle.matrix[y][x]

