import pygame
from CONSTANTS import BLOCK_SIZE

resolution = ()


def set_resolution(res):
    global resolution
    resolution = res


def load_image_block(img, size):
    global resolution
    add_size = resolution[0]*BLOCK_SIZE*0.05
    sz = resolution[1] * BLOCK_SIZE
    image = pygame.image.load(img)
    image = pygame.transform.scale(image, (size[0]*sz+add_size, size[1]*sz+add_size))
    return image.convert_alpha(), image.get_rect()


def load_image_res(img, position: tuple[int, int, int, int]):
    global resolution
    x1, y1, x2, y2 = [pos/100 for pos in position]
    image = pygame.image.load(img)
    image = pygame.transform.scale(image, ((x2-x1)*resolution[0], (y2-y1)*resolution[1])).convert_alpha()
    rect = image.get_rect()
    rect.x, rect.y = x1*resolution[0], y1*resolution[1]
    return image, rect


def load_images():
    global images
    output = {}
    for img, param in images['Assets'].items():
        if type(param) is dict:
            output[img] = {}
            for img_, param_ in param.items():
                if len(param_) == 4:
                    output[img][img_.split('.')[0]] = load_image_res(fr'Assets\{img}\{img_}', param_)
                elif len(param_) == 2:
                    output[img][img_.split('.')[0]] = load_image_block(fr'Assets\{img}\{img_}', param_)

        elif len(param) == 4:
            output[img.split('.')[0]] = load_image_res(fr'Assets\{img}', param)
        elif len(param_) == 2:
            output[img_.split('.')[0]] = load_image_block(fr'Assets\{img}', param)

    return output


images = {
    'Assets':
        {
            'background.jpg': (0, 0, 100, 100),
            'ig_background.png': (0, 0, 100, 100),
            'close.png': (94, 0, 100, 10),
            'main': {
                'play.png': (30, 60, 70, 80),
                'load.png': (5, 15, 45, 45),
                'new.png': (55, 15, 95, 45),
            },
            'box': {
                'box.png': (20, 10, 80, 90),
                'ok.png': (0, 0, 10, 8),
                'undo.png': (0, 0, 12, 8)
            },
            'Obstacles':
                {
                    'block1.png': (1, 1),
                    'block2.png': (2, 2),
                    'block3.png': (1, 1),
                    'block4.png': (1, 1),
                }
        }
}



