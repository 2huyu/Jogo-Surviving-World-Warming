import pygame
from os import listdir
from os.path import isfile, join #funções para acessar arquivos
from level_2 import *


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_bathtub_size(size):
    path = join("assets", "House", "banheiro.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Bathtub(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        bathtub = get_bathtub_size(size)
        self.name = "bathtub"
        self.image.blit(bathtub, (0, 0))



def get_closet_size(size):
    path = join("assets", "House", "closet.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Closet(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        closet = get_closet_size(size)
        self.name = "closet"
        self.image.blit(closet, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


def get_sink_size(size):
    path = join("assets", "House", "sink.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Sink(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        sink = get_sink_size(size)
        self.name = "sink"
        self.image.blit(sink, (0, 0))
        
def get_stove_size(size):
    path = join("assets", "House", "stove.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Stove(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        stove = get_stove_size(size)
        self.name = "stove"
        self.image.blit(stove, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_toilet_size(size):
    path = join("assets", "House", "toilet.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Toilet(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        toilet = get_toilet_size(size)
        self.name = "toilet"
        self.image.blit(toilet, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_table_size(size):
    path = join("assets", "House", "table.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Table(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        table = get_table_size(size)
        self.name = "table"
        self.image.blit(table, (0, 0))

def get_tree_size(size):
    path = join("assets", "House", "birch_3.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Tree(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        tree = get_tree_size(size)
        self.name = "tree"
        self.image.blit(tree, (0, 0))

def get_tree2_size(size):
    path = join("assets", "House", "jungle_tree_1.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Tree2(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        tree2 = get_tree2_size(size)
        self.name = "tree2"
        self.image.blit(tree2, (0, 0))

def get_tree3_size(size):
    path = join("assets", "House", "birch_1.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Tree3(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        tree3 = get_tree3_size(size)
        self.name = "tree3"
        self.image.blit(tree3, (0, 0))



def get_door_size(size):
    path = join("assets", "House", "Door_02.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale(surface, (200, 200))
class Door(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        door = get_door_size(size)
        self.name = "door"
        self.image.blit(door, (0, 0))

def get_bush2_size(size):
    path = join("assets", "House", "bush2.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Bush2(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        bush2 = get_bush2_size(size)
        self.name = "bush2"
        self.image.blit(bush2, (0, 0))

def get_bush1_size(size):
    path = join("assets", "House", "Bush1.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Bush1(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        bush1 = get_bush1_size(size)
        self.name = "bush1"
        self.image.blit(bush1, (0, 0))

def get_fridge_size(size):
    path = join("assets", "House", "fridge.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Fridge(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        fridge = get_fridge_size(size)
        self.name = "fridge"
        self.image.blit(fridge, (0, 0))

def get_bush3_size(size):
    path = join("assets", "House", "Bush3.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Bush3(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        bush3 = get_bush3_size(size)
        self.name = "bush3"
        self.image.blit(bush3, (0, 0))

def get_car_size(size):
    path = join("assets", "Cars", "Jeep_1", "Idle.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Car(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        car = get_car_size(size)
        self.image.blit(car, (0, 0))
        self.name = "car"
        self.mask = pygame.mask.from_surface(self.image)