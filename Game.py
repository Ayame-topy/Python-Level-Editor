import pygame
from Entities import Character, LevelEditor, MessageBox
from time import time
from CONSTANTS import *
import load_images
import os


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.width, self.height = screen.get_size()
        self.images = {}
        self.characters = []
        self.animate_event = pygame.USEREVENT
        pygame.time.set_timer(self.animate_event, 100)
        self.box = None
        self.state = None
        self.events = {}
        self.clock = pygame.time.Clock()
        self.LevelEditor = None

    def init(self):
        t = time()
        load_images.set_resolution(self.screen.get_size())
        self.images = load_images.load_images()
        self.init_message_box()
        self.set_waiting_screen()

        self.init_sounds()
        #self.init_characters()
        self.init_levels_directory()
        self.LevelEditor = LevelEditor.LevelEditor(self.screen, self.images['Obstacles'], self.set_message_box)
        del self.images['Obstacles']
        self.change_state('main')
        self.box.active = False
        self.box.reset_box()

        print('Loading time :', time()-t, 'seconds')

    def reset_events(self):
        self.events = {'CLICKED': False, 'RIGHT_CLICKED': False, 'HOLDING': self.events['HOLDING'] if 'HOLDING' in self.events else False, 'POS': pygame.mouse.get_pos()}

    def init_sounds(self):
        pygame.mixer.music.load(r'Sounds\background.mp3')
        pygame.mixer.music.play(loops=-1)

    def set_waiting_screen(self):
        self.set_message_box('Game is loading...', None)
        self.blit_elements()
        pygame.display.flip()

    def init_levels_directory(self):
        dir = os.path.join(os.getcwd(), 'Levels')
        if not os.path.exists(dir):
            os.makedirs(dir)

    def init_characters(self):
        wd = self.width * CHARACTER_WIDTH

        for i in range(1, 4):
            character = Character.Character(i, wd)
            self.characters.append(character)

    def init_message_box(self):
        self.box = MessageBox.MessageBox(*self.images['box'].values())
        del self.images['box']

    def handle_events(self):
        self.reset_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.animate_event:
                self.animate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.events['CLICKED'] = True
                    self.events['HOLDING'] = True
                elif event.button == pygame.BUTTON_RIGHT:
                    self.events['RIGHT_CLICKED'] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.events['HOLDING'] = False

    def blit_elements(self):
        self.blit_bg()
        self.blit_state_elements()
        self.blit_characters()
        self.blit_message_box()

    def change_state(self, state):
        transition_function = f'{self.state}_to_{state}'
        if hasattr(self, transition_function):
            if getattr(self, transition_function)() is None:
                self.state = state
        else:
            self.state = state

    def set_message_box(self, message: str, box_type='inf', command=None, args=()):
        self.box.set_message(message, box_type, command, args)

    def blit_characters(self):
        for char in self.characters:
            if char.showing:
                self.screen.blit(char.image, char.rect)

    def animate(self):
        for char in self.characters:
            char.animate()

    def blit_bg(self):
        self.screen.blit(*self.images['background'])
        self.screen.blit(*self.images['close'])

    def blit_message_box(self):
        if self.box.active:
            self.screen.blit(self.box.image, self.box.image_r)

    def blit_state_elements(self):
        if self.state in self.images:
            for element in self.images[self.state].values():
                self.screen.blit(*element)

    def update(self):
        self.handle_events()
        self.blit_elements()
        if not self.box.active:
            update_function = self.state + '_update'
            if hasattr(self, update_function):
                getattr(self, update_function)()
        self.global_update()

    def global_update(self):
        events = self.events
        close, close_r = self.images['close']
        pos = self.events['POS']

        if close_r.collidepoint(pos):
            s = pygame.Surface(close.get_size())
            s.fill('red')
            s.blit(close, (0, 0))
            self.screen.blit(s, close_r)

        if self.events['CLICKED']:
            if close_r.collidepoint(pos):
                self.set_message_box('Are you sure you want to quit ?', 'choice', self.close)
            if self.box.active:
                if self.box.image_r.collidepoint(pos):
                    self.box.on_click(pos)

        self.clock.tick(60)

    def main_update(self):
        images = self.get_state_images()

        if self.events['CLICKED']:
            _, new_r = images['new']
            _, play_r = images['play']
            _, load_r = images['load']
            pos = self.events['POS']

            if new_r.collidepoint(pos):
                self.change_state('edit')

            elif play_r.collidepoint(pos):
                pass

            elif load_r.collidepoint(pos):
                pass

    def main_to_play(self):
        pass

    def main_to_edit(self):
        self.switch_background()
        self.LevelEditor.set_new_level()
        self.set_message_box('Tips : You can right click on an obstacle to remove it')

    def edit_update(self):
        self.LevelEditor.update(self.events)

    def get_state_images(self):
        return self.images[self.state]

    def close(self):
        self.running = False

    def switch_background(self):
        self.images['background'], self.images['ig_background'] = self.images['ig_background'], self.images['background']
