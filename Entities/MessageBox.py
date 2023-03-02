import pygame
from CONSTANTS import MAX_LINE_BOX_LETTERS, TEXT_COLOR


class MessageBox:
    def __init__(self, img, ok, undo):
        self.init_image, self.image_r = img
        self.image = self.init_image.copy()
        self.ok, self.ok_r = ok
        self.undo, self.undo_r = undo
        self.type = 'inf'
        self.command = None
        self.args = None
        self.active = False
        self.font = pygame.font.SysFont('Forte', 300)

    def reset_box(self):
        self.image = self.init_image.copy()

    def set_message(self, message, box_type, command, args):
        self.reset_box()
        self.command = command
        self.type = box_type
        self.active = True
        self.args = args

        split = list(message.split())
        lines = ['']
        l = 0

        for _ in range(len(split)):
            l_ = len(split[0])
            if l + l_ > MAX_LINE_BOX_LETTERS:
                lines.append(split.pop(0) + ' ')
                l = l_
            else:
                lines[-1] += split.pop(0) + ' '
                l += l_
        y = 0
        box = self.image
        hgt = 0
        for l in lines:
            l = self.font.render(l, True, TEXT_COLOR)
            if hgt != 0:
                l = pygame.transform.scale(l, (l.get_width()/l.get_height()*hgt, hgt))
            else:
                l = pygame.transform.scale(l, (box.get_width() * 0.7, box.get_width() * 0.7 / l.get_width() * l.get_height()))
            if hgt == 0:
                hgt = l.get_height()
            box.blit(l, (box.get_width()*0.01+box.get_width() / 2 - l.get_width() / 2, box.get_height() * 0.3 + y))
            y += l.get_height()

        y = self.image.get_height()*0.7

        if box_type == 'inf':
            self.ok_r.x, self.ok_r.y = self.image.get_width()/2-self.ok.get_width()/2, y
            self.image.blit(self.ok, self.ok_r)
        elif box_type == 'choice':
            self.ok_r.x, self.ok_r.y = self.image.get_width() / 4 - self.ok.get_width() / 2, y
            self.undo_r.x, self.undo_r.y = self.image.get_width()*0.75 - self.undo.get_width()/2, y
            self.image.blit(self.ok, self.ok_r)
            self.image.blit(self.undo, self.undo_r)

    def on_click(self, pos):
        pos = pos[0] - self.image_r.x, pos[1] - self.image_r.y

        if self.type == 'inf':
            if self.ok_r.collidepoint(pos):
                self.active = False
        elif self.type == 'choice':
            if self.undo_r.collidepoint(pos):
                self.active = False
            elif self.ok_r.collidepoint(pos):
                self.call_command()
                self.active = False

    def call_command(self):
        self.command(*self.args)
