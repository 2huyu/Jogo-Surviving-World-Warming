import pygame
from os import listdir
from os.path import isfile, join
import random
from button import *
from pause import draw_pause_menu

pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Flood Flow Enchente")

WIDTH, HEIGHT = 1280, 720
FPS = 120
PLAYER_VEL = 6

window = pygame.display.set_mode((WIDTH, HEIGHT))
level_bg_music = pygame.mixer.music.load('assets/Audio/level_music.wav')
pygame.mixer.music.play()
pygame.mixer.music.play(-1)

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "TerrainCidade.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_block_2(size):
    path = join("assets", "Terrain", "TerrainCidade.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(144, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return surface


def get_car_size(size):
    path = join("assets", "Cars", "Jeep_1", "Idle.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_ship_size(size):
    path = join("assets", "Ship", "ship.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.life = 10
        self.god = False
        self.god_timer = 500
        self.hit_timer = 0
        self.jump_sound = pygame.mixer.Sound('assets/Audio/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('assets/Audio/hit.wav')

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_sound.play()
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def die(self):
        self.life = 0

    def make_hit(self):
        self.hit = True
        if self.hit:
            self.take_hit()
            self.god_period()

    def take_hit(self):
        if not self.god:
            self.hit_sound.play()
            self.life -= 1
            self.god = True
            self.hit_timer = pygame.time.get_ticks()

    def god_period(self):
        if self.god:
            actual_time = pygame.time.get_ticks()
            if actual_time - self.hit_timer >= self.god_timer:
                self.god = False

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
            self.move(self.x_vel, self.y_vel)

            if self.hit:
                self.hit_count += 1
            if self.hit_count > fps * 2:
                self.hit = False
                self.hit_count = 0

            self.fall_count += 1
            self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        if self.rect.y > 650:
            from main import death
            death()
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Car(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        car = get_car_size(size)
        self.image.blit(car, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Ship(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        ship = get_ship_size(size)
        self.image.blit(ship, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = "ship"
class Block_2(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_2 = get_block_2(size)
        self.image.blit(block_2, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Wave(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SPRITES = load_sprite_sheets("Waves", "ground", 800, 250)
    ANIMATION_DELAY = 9

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 20
        self.y_vel = 0
        self.mask = None
        self.name = "wave"
        self.animation_count = 0

    def loop(self):
            self.rect.x += self.x_vel
            self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "waves"

        sprite_sheet_name = sprite_sheet
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.sprite = pygame.transform.rotate(self.sprite, 270)
        self.sprite = pygame.transform.scale(self.sprite, (1500, 540))
        self.animation_count += 1
        if self.rect.x >= 7500:
            self.rect.x = -900
        self.update()
        

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))


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


class Saw(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "saw")
        self.saw = load_sprite_sheets("Traps", "Saw", width, height)
        self.image = self.saw["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
            sprites = self.saw[self.animation_name]
            sprite_index = (self.animation_count //
                            self.ANIMATION_DELAY) % len(sprites)
            self.image = sprites[sprite_index]
            self.animation_count += 1

            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pygame.mask.from_surface(self.image)

            if self.animation_count // self.ANIMATION_DELAY > len(sprites):
                self.animation_count = 0


class Rain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rain_img
        self.rect = self.image.get_rect()
        self.speedx = 3
        self.speedy = random.randint(5, 25)
        self.rect.x = random.randint(-100, WIDTH)
        self.rect.y = random.randint(-HEIGHT, -5)

    def update(self):
            if self.rect.bottom > HEIGHT:
                self.speedx = 3
                self.speedy = random.randint(5, 25)
                self.rect.x = random.randint(-WIDTH, WIDTH)
                self.rect.y = random.randint(-HEIGHT, -5)

            self.rect.x = self.rect.x + self.speedx
            self.rect.y = self.rect.y + self.speedy

def get_poste_size(size):
    path = join("assets", "House", "poste.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Poste(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        poste = get_poste_size(size)
        self.name = "poste"
        self.image.blit(poste, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_spike_size(size):
    path = join("assets", "Traps", "Spikes", "idle.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Spike(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        spike = get_spike_size(size)
        self.name = "spike"
        self.image.blit(spike, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_spikeball_size(size):
    path = join("assets", "Traps", "Spiked Ball", "Spiked Ball.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Spikeball(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        spikeball = get_spikeball_size(size)
        self.name = "spikeball"
        self.image.blit(spikeball, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_spikeruin_size(size):
    path = join("assets", "Traps", "Spike Head", "Idle.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 200, size)
    surface.blit(image, (0, 0), rect)
    return surface
class Spikeruin(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        spikeruin = get_spikeruin_size(size)
        self.name = "spikeruin"
        self.image.blit(spikeruin, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_tree_size(size):
    path = join("assets", "Traps", "middle_lane_tree1.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class Tree(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        tree = get_tree_size(size)
        self.name = "tree"
        self.image.blit(tree, (0, 0))

def get_background(name):
    image = pygame.image.load(join("assets", "city", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 100):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x, offset_y, PAUSE):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)

    x = 30
    y = 30
    spacing = 20
    life_width = 60
    life_height = 20
    life_color = (0, 255, 0)  # cor das vidas restantes
    lost_life_color = (0, 0, 0)  # cor das vidas perdidas
    for i in range(player.life):
        pygame.draw.rect(window, life_color, (x, y, life_width, life_height))
        x += spacing
    for i in range(player.life, 5):
        pygame.draw.rect(window, lost_life_color,
                         (x, y, life_width, life_height))
        x += spacing
    
    if PAUSE:
        draw_pause_menu(window)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if obj.name == "tree":
                continue
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    from main import death, victory
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)
    # if keys[pygame.K_ESCAPE]:

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "spikeball":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "spike":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "saw":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "wave":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "spikeruin":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "ship":
            victory()

rain_img = pygame.image.load('assets/Background/rain.png')
rain_img = pygame.transform.scale(rain_img, (16, 16))
rain_group = pygame.sprite.Group()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("bg_nivel_1.png")
    PAUSE = False
    block_size = 96
    saw_size = 96
    block_size_2 = 32
    wave_size = 200
    car_1_size = 84
    ship_size = 170

    player = Player(500, 100, 50, 50)

    ship = Ship(WIDTH * 6, HEIGHT - ship_size, 720)

    wave_1 = Wave(-1000, HEIGHT - wave_size * 2, 1000, 500)
    for i in range(150):
        rain = Rain()
        rain_group.add(rain)

    # carros
    carro_1 = Car(3800, HEIGHT - car_1_size * 2 - 64, 720)
    carro_2 = Car(4200, HEIGHT - car_1_size * 2 - 64, 720)
    carro_3 = Car(380, HEIGHT - 500, 720)

    poste = Poste(950, HEIGHT - 480, 720)

    spike_1 = Spike(1250, HEIGHT - 125,720)
    # fire
    fire = Spikeball(700, HEIGHT - block_size - 64,  320)
    fire_2 = Spikeball(2140, HEIGHT - block_size - 64,  320)
    fire_3 = Spikeball(2330, HEIGHT - block_size - 64,  320)
    fire_4 = Spikeball(2530, HEIGHT - block_size - 64, 320)
    fire_5 = Spikeball(2720, HEIGHT - block_size - 64,320)
    fire_6 = Spike(3200, HEIGHT - block_size - 415, 320)
    fire_7 = Spikeball(3650, HEIGHT - block_size - 154, 320)
    fire_8 = Spikeball(3686, HEIGHT - block_size - 154, 320)
    fire_9 = Spikeball(3722, HEIGHT - block_size - 64,  320)
    fire_10 = Spikeball(3758, HEIGHT - block_size - 64, 320)


    # saw
    saw = Saw(4094, HEIGHT - saw_size - 74, 38, 38)
    saw.on()
    saw_1 = Saw(4128, HEIGHT - saw_size * 2 - 74, 38, 38)
    saw_1.on()
    saw_2 = Saw(5900, HEIGHT - saw_size * 3 - 74, 38, 38)
    saw_2.on()
    saw_3 = Saw(4094, HEIGHT - saw_size - 74, 38, 38)
    saw_3.on()
    saw_4 = Saw(5250, HEIGHT - block_size*3, 38, 38)
    saw_4.on()
    

    # esse for de baixo vai colocar mais blocos no chão
    floor_1 = [Block(i * block_size, HEIGHT - block_size, block_size)
               for i in range(-WIDTH // block_size, (WIDTH * 6) // block_size)]
    floor_2 = [Block_2(n * block_size_2, HEIGHT, block_size_2)
               for n in range(-WIDTH // block_size_2, (WIDTH * 6) // block_size_2)]
    floor_3 = [Block_2(n * block_size_2, HEIGHT + block_size_2, block_size_2)
               for n in range(-WIDTH // block_size_2, (WIDTH * 6) // block_size_2)]
    floor_4 = [Block_2(n * block_size_2, HEIGHT + block_size_2 + block_size_2, block_size_2)
               for n in range(-WIDTH // block_size_2, (WIDTH * 6) // block_size_2)]

    # um desses aqui coloca blocos na tela
    objects = [*floor_1, *floor_2, *floor_3, *floor_4,
               #    distancia X altura
               Car(-100, HEIGHT - block_size * 2.3, 720),
               Block(block_size * 3, HEIGHT - block_size * 3, block_size), fire,
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), poste,
               Block(block_size * 4, HEIGHT - block_size * 4, block_size), carro_3,
               Block(block_size * 5, HEIGHT - block_size * 4, block_size), spike_1,
               Block(block_size * 6, HEIGHT - block_size * 4, block_size),
               Block(block_size * 6, HEIGHT - block_size * 2, block_size),
               Block(block_size * 8, HEIGHT - block_size * 2, block_size),
               Block(block_size * 11, HEIGHT - block_size * 4, block_size),
               Block(block_size * 11, HEIGHT - block_size * 3, block_size),
                Car(1450, HEIGHT - block_size * 2.3, 720),
               Block(block_size * 17, HEIGHT - block_size * 4, block_size),
               Block(block_size * 20, HEIGHT - block_size * 5, block_size),

               Block(block_size * 21, HEIGHT - block_size * 2, block_size), fire_2,
               Block(block_size * 23, HEIGHT - block_size * 2, block_size), fire_3,
               Block(block_size * 25, HEIGHT - block_size * 2, block_size), fire_4,
               Block(block_size * 27, HEIGHT - block_size * 2, block_size), fire_5,
               Block(block_size * 29, HEIGHT - block_size * 2, block_size),

               Block(block_size * 33, HEIGHT - block_size * 3, block_size), fire_6,
               Block(block_size * 33, HEIGHT - block_size * 4, block_size),
               Block(block_size * 33, HEIGHT - block_size * 5, block_size),

               Block(block_size * 37, HEIGHT - block_size * 2, block_size),
               Block(block_size * 37, HEIGHT - block_size * 3, block_size),
               Block(block_size * 37, HEIGHT - block_size * 4, block_size),
               Block(block_size * 37, HEIGHT - block_size * 5, block_size),
               Block(block_size * 37, HEIGHT - block_size * 7, block_size),
               Block(block_size * 37, HEIGHT - block_size * 8, block_size),
               Block(block_size * 38, HEIGHT - block_size * 2, block_size),

               Block(block_size * 36, HEIGHT - block_size * 2, block_size),
               Block(block_size * 34, HEIGHT - block_size * 3, block_size),
               Block(block_size * 35, HEIGHT - block_size * 5, block_size),
               fire_7, fire_8, fire_9, fire_10, carro_1, saw, saw_1, carro_2,

               Block(block_size * 11, HEIGHT - block_size * 4, block_size),
               Block(block_size * 11, HEIGHT - block_size * 4, block_size),
               Block(block_size * 11, HEIGHT - block_size * 4, block_size),
               Block(block_size * 11, HEIGHT - block_size * 4, block_size),
               Block(block_size * 11, HEIGHT - block_size * 4, block_size),ship,
               Block(block_size * 11, HEIGHT - \
                     block_size * 4, block_size), wave_1, 
                Block(block_size * 50, HEIGHT - block_size * 2, block_size),
                Block(block_size * 49, HEIGHT - block_size * 3, block_size),
                Block(block_size * 50, HEIGHT - block_size * 4, block_size),
                Block(block_size * 49, HEIGHT - block_size * 5, block_size),
                Poste(5100, HEIGHT - 480, 720),
                saw_4,
                Car(5400, HEIGHT - block_size * 2.3, 720),
                Tree(5800, HEIGHT - block_size * 3.6, 720),
                Block(block_size * 60, HEIGHT - block_size * 3, block_size),
                saw_2,
                Block(block_size * 62, HEIGHT - block_size * 5, block_size),
                saw_3,
                Block(block_size * 65, HEIGHT - block_size * 6, block_size),
                Poste(6600, HEIGHT - 480, 720),

                Block(block_size * 73, HEIGHT - block_size * 5, block_size),
                Block(block_size * 74, HEIGHT - block_size * 5, block_size),
                Block(block_size * 74, HEIGHT - block_size * 6, block_size),
                Block(block_size * 74, HEIGHT - block_size * 7, block_size),
                Block(block_size * 74, HEIGHT - block_size * 8, block_size),
                Block(block_size * 72, HEIGHT - block_size * 7, block_size),
                Block(block_size * 71, HEIGHT - block_size * 7, block_size),
                Block(block_size * 71, HEIGHT - block_size * 8, block_size),
                Block(block_size * 71, HEIGHT - block_size * 9, block_size),
                Block(block_size * 69, HEIGHT - block_size * 10, block_size),
                Spikeruin(6800, HEIGHT - block_size * 11, 720),
                Block(block_size * 72, HEIGHT - block_size * 11, block_size),
                Spikeruin(7120, HEIGHT - block_size * 12, 720),
                Block(block_size * 75, HEIGHT - block_size * 12, block_size),
                Spike(7000, HEIGHT - 125, 200),
                Spike(7150, HEIGHT - 125, 200),
                Spike(7300, HEIGHT - 125, 200),
                Spike(7400, HEIGHT - 125, 200),
                Spike(7500, HEIGHT - 125, 200),
                Spike(6800, HEIGHT - 125, 200),
               ]

    # objects.extend([wave_1])

    # muda onde a tela começa
    offset_x = player.rect.x - 400
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 100

    run = True
    while run:
        
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2 :
                    player.jump()
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_w and player.jump_count < 2 :
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    PAUSE = not PAUSE
        
        if PAUSE == False:
            player.loop(FPS)
            wave_1.loop()
            saw.loop()
            saw_1.loop()
            saw_2.loop()
            saw_3.loop()
            saw_4.loop()
            handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, offset_y, PAUSE)

        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height -50) and player.y_vel > 0) or (
        (player.rect.top - offset_y <= (scroll_area_height + 100)) and player.y_vel < 0): 
            offset_y += player.y_vel # a janela carrega elementos criados conforme jogador vai andando

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        rain_group.update()
        rain_group.draw(window)
        pygame.display.flip()
    pygame.mixer.quit()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
