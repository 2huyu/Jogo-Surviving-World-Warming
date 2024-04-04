import random
import pygame
from os import listdir
from os.path import isfile, join
from button import *
from pause import draw_pause_menu


pygame.init()

pygame.display.set_caption("Avalanche")

WIDTH, HEIGHT = 1280, 680
FPS = 60
PLAYER_VEL = 7


window = pygame.display.set_mode((WIDTH, HEIGHT))


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
    rect = pygame.Rect(96, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_chopper_size(size):
    path = join("assets", "Chopper", "chopper.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 700, 331)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale(surface,(420,420))

def get_block_2(size):
    path = join("assets", "Terrain", "TerrainCidade.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(144, 64, size, size)
    surface.blit(image, (0, 0), rect)
    return surface


def get_car_size(size):
    path = join("assets", "Cars", "Jeep_1", "Idle.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, 720, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
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

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        if self.hit:
            self.take_hit()
            self.god_period()

    def take_hit(self):
        if not self.god:
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
        if self.rect.y > 600:
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


class Block_2(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block_2 = get_block_2(size)
        self.image.blit(block_2, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Chopper(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        chopper = get_chopper_size(size)
        self.image.blit(chopper, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = "chopper"

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


def get_background(name):
    image = pygame.image.load(join("assets", "city", name)).convert()
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 100):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x, offset_y, pause):
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

    for i in range(player.life, 10):
        pygame.draw.rect(window, lost_life_color,
                         (x, y, life_width, life_height))
        x += spacing
    
    if pause:
        draw_pause_menu(window)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
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
    from main import victory, death
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

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        from main import death
        if obj and obj.name == "fire":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "saw":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "avalanche":
            player.make_hit()
            if player.life <= 0:
                death()
        if obj and obj.name == "chopper":
            victory()


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


rain_img = pygame.image.load('assets/Background/snow.png')
rain_img = pygame.transform.scale(rain_img, (16, 16))
rain_group = pygame.sprite.Group()


class Avalanche(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SPRITES = load_sprite_sheets("Disaster", "Avalanche", 800, 500)
    ANIMATION_DELAY = 9

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 20
        self.y_vel = 0
        self.mask = None
        self.name = "avalanche"
        self.animation_count = 0

    def loop(self):
        self.rect.x += self.x_vel
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "Avalanche"

        sprite_sheet_name = sprite_sheet
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.sprite = pygame.transform.rotate(self.sprite, 270)
        self.sprite = pygame.transform.scale(self.sprite, (1000, 540))
        self.animation_count += 1
        if self.rect.x >= 6200:
            self.rect.x = -900
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("bg_nivel_3.png")
    pause = False
    block_size = 96
    saw_size = 96
    block_size_2 = 32
    car_1_size = 84
    wave_size = 200
    chopper_size = 330

    player = Player(100, 100, 50, 50)
    avalanche = Avalanche(-1000, HEIGHT - wave_size * 2, 1000, 500)
    chopper = Chopper(6990, HEIGHT - (chopper_size * 3) - 160, 720)

    for i in range(150):
        rain = Rain()
        rain_group.add(rain)
    # carros
    carro_1 = Car(3800, HEIGHT - car_1_size * 2 - 64, 720)
    carro_2 = Car(4180, HEIGHT - car_1_size * 2 - 64, 720)

    # fire
    fire = Fire(900, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    fire_2 = Fire(2140, HEIGHT - block_size - 64, 16, 32)
    fire_2.on()
    fire_3 = Fire(2330, HEIGHT - block_size - 64, 16, 32)
    fire_3.on()
    fire_4 = Fire(2530, HEIGHT - block_size - 64, 16, 32)
    fire_4.on()
    fire_5 = Fire(2720, HEIGHT - block_size - 64, 16, 32)
    fire_5.on()

    fire_6 = Fire(3086, HEIGHT - block_size - 64, 16, 32)
    fire_6.on()
    fire_7 = Fire(3495, HEIGHT - block_size - 64, 16, 32)
    fire_7.on()
    fire_8 = Fire(4158, HEIGHT - block_size - 64, 16, 32)
    fire_8.on()
    fire_9 = Fire(4930, HEIGHT - block_size - 64, 16, 32)
    fire_9.on()
    fire_10 = Fire(5700, HEIGHT - block_size - 64, 16, 32)
    fire_10.on()

    # saw
    saw = Saw(1500, HEIGHT - saw_size - 240, 38, 38)
    saw.on()
    saw_1 = Saw(1570, HEIGHT - saw_size - 160, 38, 38)
    saw_1.on()
    saw_2 = Saw(3755, HEIGHT - saw_size - 74, 38, 38)
    saw_2.on()
    saw_3 = Saw(4520, HEIGHT - saw_size - 74, 38, 38)
    saw_3.on()
    saw_4 = Saw(5280, HEIGHT - saw_size - 74, 38, 38)
    saw_4.on()

    # esse for de cima vai colocar mais blocos no chão
    floor_1 = [Block(i * block_size, HEIGHT - block_size, block_size)
               for i in range(-WIDTH // block_size, (WIDTH * 5) // block_size)]
    floor_2 = [Block_2(n * block_size_2, HEIGHT, block_size_2)
               for n in range(-WIDTH // block_size_2, (WIDTH * 5) // block_size_2)]
    floor_3 = [Block_2(n * block_size_2, HEIGHT + block_size_2, block_size_2)
               for n in range(-WIDTH // block_size_2, (WIDTH * 5) // block_size_2)]
    floor_4 = [Block_2(n * block_size_2, HEIGHT + block_size_2 + block_size_2, block_size_2)
               for n in range(-WIDTH // block_size_2, (WIDTH * 5) // block_size_2)]

    # um desses aqui coloca blocos na tela
    objects = [
        *floor_1, *floor_2, *floor_3, *floor_4,
        #    distancia X altura
        # primeiro nível de blocos acima do chão
        fire, fire_2, fire_3, fire_4, fire_5, fire_6, fire_7, fire,
        fire_8, fire_9,
        fire_10,

        saw, saw_1, saw_2, saw_3, saw_4,
        Block(0, HEIGHT - block_size * 2, block_size),
        Block(block_size * 5, HEIGHT - block_size * 2, block_size),
        Block(block_size * 12, HEIGHT - block_size * 2, block_size),
        # segundo nível de blocos acima do chão
        Block(block_size * 3, HEIGHT - block_size * 3, block_size),
        Block(block_size * 7, HEIGHT - block_size * 3, block_size),
        Block(block_size * 13, HEIGHT - block_size * 3, block_size),
        Block(block_size * 19, HEIGHT - block_size * 3, block_size),
        Block(block_size * 22, HEIGHT - block_size * 3, block_size),
        Block(block_size * 24, HEIGHT - block_size * 3, block_size),
        Block(block_size * 26, HEIGHT - block_size * 3, block_size),
        Block(block_size * 28, HEIGHT - block_size * 3, block_size),
        # terceiro nível de blocos acima do chão
        Block(block_size * 3, HEIGHT - block_size * 4, block_size),
        Block(block_size * 4, HEIGHT - block_size * 4, block_size),
        Block(block_size * 5, HEIGHT - block_size * 4, block_size),
        Block(block_size * 6, HEIGHT - block_size * 4, block_size),
        Block(block_size * 7, HEIGHT - block_size * 4, block_size),
        Block(block_size * 18, HEIGHT - block_size * 4, block_size),
        Block(block_size * 14, HEIGHT - block_size * 4, block_size),
        # quarto nível de blocos acima do chão
        Block(block_size * 17, HEIGHT - block_size * 5, block_size),

        # parede zig zag
        Block(block_size * 34, HEIGHT - block_size * 2, block_size),
        Block(block_size * 33, HEIGHT - block_size * 3, block_size),
        Block(block_size * 34, HEIGHT - block_size * 4, block_size),
        Block(block_size * 33, HEIGHT - block_size * 5, block_size),
        Block(block_size * 34, HEIGHT - block_size * 6, block_size),
        Block(block_size * 33, HEIGHT - block_size * 7, block_size),
        Block(block_size * 34, HEIGHT - block_size * 8, block_size),
        Block(block_size * 33, HEIGHT - block_size * 9, block_size),


        Block(block_size * 37, HEIGHT - block_size * 9, block_size),
        Block(block_size * 43, HEIGHT - block_size * 9, block_size),
        Block(block_size * 49, HEIGHT - block_size * 9, block_size),
        Block(block_size * 55, HEIGHT - block_size * 9, block_size),
        # Block(block_size * 61, HEIGHT - block_size * 3, block_size),


        Block(block_size * 56, HEIGHT - block_size * 8, block_size),
        Block(block_size * 57, HEIGHT - block_size * 7, block_size),
        Block(block_size * 58, HEIGHT - block_size * 6, block_size),
        Block(block_size * 59, HEIGHT - block_size * 5, block_size),
        Block(block_size * 60, HEIGHT - block_size * 4, block_size),
        Block(block_size * 61, HEIGHT - block_size * 3, block_size),
        Block(block_size * 62, HEIGHT - block_size * 2, block_size),
        avalanche,
        Block(block_size * 66, HEIGHT - block_size * 1, block_size),
        Block(block_size * 68, HEIGHT - block_size * 3, block_size),
        Block(block_size * 69, HEIGHT - block_size * 4, block_size),
        Block(block_size * 71, HEIGHT - block_size * 6, block_size),
        Block(block_size * 72, HEIGHT - block_size * 7, block_size),
        Block(block_size * 73, HEIGHT - block_size * 9, block_size),
        Block(block_size * 74, HEIGHT - block_size * 10, block_size),
        Block(block_size * 75, HEIGHT - block_size * 10, block_size),chopper
    ]

    # change where the screen starts
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
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_w and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
        if pause == False:
            player.loop(FPS)
            fire.loop()
            fire_2.loop()
            fire_3.loop()
            fire_4.loop()
            fire_5.loop()
            fire_6.loop()
            fire_7.loop()
            fire_8.loop()
            fire_9.loop()
            fire_10.loop()
            saw.loop()
            saw_1.loop()
            saw_2.loop()
            saw_3.loop()
            saw_4.loop()
            avalanche.loop()
            handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, offset_y, pause)

        if pause == False:
            if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or (
                    (player.rect.top - offset_y <= (scroll_area_height + 100)) and player.y_vel < 0):
                offset_y += player.y_vel

            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel

        rain_group.update()
        rain_group.draw(window)
        pygame.display.flip()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
