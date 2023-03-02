import pygame
from Entities import Level, Obstacle, Mob
from CONSTANTS import BLOCK_SIZE, EDIT_MENU_COLOR
import math


class LevelEditor:
    obstacles_categories = ('block', )
    tips = {'unselect_obstacle': 'You can unselect the selected obstacle by right clicking'}

    def __init__(self, screen, obstacles, box_function):
        self.screen = screen
        self.level = None
        self.obstacles = {}
        self.init_obstacles(obstacles)
        self.selected_obstacle = None
        self.box_function = box_function
        self.current_category = self.obstacles_categories[0]
        self.menu = {}
        self.init_menu()

    def is_tips_to_show(self, tips):
        return tips in self.tips

    def show_tips(self, tips):
        if self.is_tips_to_show(tips):
            self.box_function('Tips : ' + self.tips[tips])
            del self.tips[tips]

    def init_obstacles(self, obstacles):
        block_sz = self.screen.get_height()*BLOCK_SIZE

        for category in self.obstacles_categories:
            self.obstacles[category] = pygame.sprite.Group()

        for name, (surf, rect) in obstacles.items():
            obstacle = Obstacle.Obstacle(name, surf, (round(surf.get_width()/block_sz), round(surf.get_height()/block_sz)))
            for category in self.obstacles:
                if name.startswith(category):
                    self.obstacles[category].add(obstacle)

    def init_menu(self):
        x, y = self.screen.get_size()
        menu = pygame.Surface((x, y*0.4), pygame.SRCALPHA)
        menu.fill(EDIT_MENU_COLOR)
        rect = menu.get_rect()
        rect.y = y - menu.get_height()
        self.menu['init_menu'] = menu
        self.menu['menu'] = (menu.copy(), rect)

        x = x*0.1
        for category_name, category in self.obstacles.items():
            sprite = [obstacle for obstacle in category][0].image
            self.menu[category_name] = pygame.Rect((x, 0, *sprite.get_size()))
            menu.blit(sprite, (x, 0))
            x += sprite.get_width()

            x_ = 0
            for obstacle in category:
                obstacle.set_pos((x_, menu.get_height()-obstacle.image.get_height()))
                x_ += obstacle.image.get_width()

        self.update_menu()

    def update_menu(self):
        menu = self.menu['init_menu'].copy()
        self.menu['menu'] = menu, self.menu['menu'][1]
        self.obstacles[self.current_category].draw(menu)

    def change_category(self, category):
        self.current_category = category
        self.update_menu()

    def set_new_level(self):
        wd, hgt = self.screen.get_size()
        b_sz = self.screen.get_height()*BLOCK_SIZE
        size = math.ceil(self.screen.get_width()/b_sz), math.ceil(self.screen.get_height()/b_sz)
        print(size)
        self.set_level(Level.Level(size))
        block = {obstacle.name: obstacle for obstacle in self.obstacles['block']}['block2']
        obstacle = self.copy_obstacle(block)
        for x in range(0, math.ceil(wd/(hgt*BLOCK_SIZE)), 2):
            self.set_obstacle_rect((x, 8), obstacle)
            self.add_obstacle(obstacle)

    def set_level(self, level:  Level.Level):
        self.level = level

    def blit_menu(self):
        if self.selected_obstacle is None:
            self.screen.blit(*self.menu['menu'])

    def draw_elements(self):
        self.show_grid()
        self.level.group.draw(self.screen)
        self.show_selected_obstacle()
        self.blit_menu()

    def show_grid(self):
        sz = self.screen.get_height()*BLOCK_SIZE
        rat = self.screen.get_width()/self.screen.get_height()
        for y in range(round(1/BLOCK_SIZE)):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y*sz), (self.screen.get_width(), y*sz))
        for x in range(round(1/BLOCK_SIZE*rat)):
            pygame.draw.line(self.screen, (30, 30, 30), (x*sz, 0), (x*sz, self.screen.get_height()))

    def update(self, events):
        self.draw_elements()
        self.global_update(events)
        self.on_click(events)

    def global_update(self, events):
        x, y = events['POS']
        if self.selected_obstacle is not None:
            x_pos, y_pos = self.mouse_pos_to_blocks((x, y))
            self.set_obstacle_rect((x_pos, y_pos))

    def set_obstacle_rect(self, pos, obstacle=None):
        if obstacle is None: obstacle = self.selected_obstacle
        x, y = pos
        x, y = x*self.screen.get_height()*BLOCK_SIZE, y*self.screen.get_height()*BLOCK_SIZE
        x, y = x*0.99, y*0.99
        obstacle.set_row_column(pos)
        obstacle.set_pos((x, y))

    def show_selected_obstacle(self):
        if self.selected_obstacle is not None:
            self.screen.blit(self.selected_obstacle.image, self.selected_obstacle.rect)

    def get_current_category_group(self):
        return self.obstacles[self.current_category]

    def on_click(self, events):
        pos = events['POS']
        if events['CLICKED']:
            if self.selected_obstacle is None:
                menu, menu_r = self.menu['menu']
                if menu_r.collidepoint(pos):
                    pos_ = pos[0], pos[1] - menu_r.y
                    for obstacle in self.get_current_category_group():
                        if obstacle.rect.collidepoint(pos_):
                            self.set_selected_obstacle(obstacle)
            else:
                self.add_obstacle(self.selected_obstacle)
        elif events['RIGHT_CLICKED']:
            if self.selected_obstacle is None:
                self.level.clear_block(self.mouse_pos_to_blocks(pos))
            else:
                self.selected_obstacle = None

    def copy_obstacle(self, obstacle):
        new_obstacle = Obstacle.Obstacle(obstacle.name, obstacle.image, obstacle.size)
        self.set_obstacle_rect((obstacle.x, obstacle.y), new_obstacle)
        return new_obstacle

    def mouse_pos_to_blocks(self, pos):
        x_pos = math.floor(abs(pos[0] + 1) / (self.screen.get_height() * BLOCK_SIZE))
        y_pos = math.floor(abs(pos[1] + 1) / (self.screen.get_height() * BLOCK_SIZE))
        return x_pos, y_pos

    def set_selected_obstacle(self, obstacle):
        self.selected_obstacle = self.copy_obstacle(obstacle)
        self.show_tips('unselect_obstacle')

    def add_obstacle(self, obstacle):
        self.level.add_obstacle(self.copy_obstacle(obstacle))
