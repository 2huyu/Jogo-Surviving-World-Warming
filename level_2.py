import os
import random
import math
import pygame
import sys
from os import listdir
from os.path import isfile, join #funções para acessar arquivos
from button import *
from pause import draw_pause_menu

pygame.init()

pygame.display.set_caption("Heatwaves")

WIDTH, HEIGHT = 1280, 720

FPS = 180
PLAYER_VEL = 7
countdown = 0


window = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("assets/city/bg_nivel_2.png")

calor_imagem = pygame.Surface((1280,720), pygame.SRCALPHA)  
calor_imagem.fill((255, 228, 132, 60))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False): # é dinâmico para acessar qualquer tipo de sprite, a direction serve para definir se a imagem possui multiplos sprites ou só 1
    path = join("assets", dir1, dir2)   # acessa a pasta
    images = [f for f in listdir(path) if isfile(join(path, f))] #acessa todos os nomes de arquivos dentro de uma pasta

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface)) # dobra os sprites de 32px para 64px

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
def get_wood_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
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
        self.calor = 0
        self.life = 20
        self.invincible = False
        self.god_timer = 500
        self.hit_timer = 0
        self.jump_sound = pygame.mixer.Sound('assets/Audio/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('assets/Audio/hit.wav')

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.jump_sound.play()
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

    def take_hit(self):
        if not self.invincible:
            self.life -= 1
            self.hit_sound.play()
            self.invincible = True
            self.hit_timer = pygame.time.get_ticks()

    def god_period(self):
        if self.invincible:
            actual_time = pygame.time.get_ticks()
            if actual_time - self.hit_timer >= self.god_timer:
                self.invincible = False

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

    def draw(self, win, offset_x,  offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
        self.sprite = None

    def draw(self, win, offset_x,  offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Wood(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        wood_block = get_wood_block(size)
        self.image.blit(wood_block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)



def draw(window, player, objects, offset_x,  offset_y, countdown, pause):
    window.blit(background, (0,0))

    for obj in objects:
        obj.draw(window, offset_x,  offset_y)

    player.draw(window, offset_x,  offset_y)
    


    x_life = 30
    y_life = 30
    spacing_life = 20
    actual_life = (0, 255, 0)  # cor das vidas restantes
    max_life = (0, 0, 0)  # cor das vidas perdidas

    x_heat = 30
    y_heat = 90
    spacing_heat = 0.5
    
    for i in range(player.life):
        pygame.draw.rect(window, actual_life, (x_life, y_life, 60, 20))
        x_life += spacing_life
    for i in range(player.life, 20):
        if x_life < 400:
            pygame.draw.rect(window, max_life, (x_life, y_life, 60, 20))
            x_life += spacing_life

        #barra de calor atual
    for i in range(player.calor):
        pygame.draw.rect(window, (255, 228, 132), (x_heat, y_heat, 60, 20))
        if x_heat >= 400:
            x_heat = 400
        else:
            x_heat += spacing_heat
        #barra maxima
    for i in range(player.calor, 800): 
        pygame.draw.rect(window, (0, 0 , 0), (x_heat, y_heat, 1, 20))
        x_heat += spacing_heat

    if countdown < 175:
        window.blit(calor_imagem, (0,0))
    text = get_font(75).render(str(int(countdown)), True, (255, 255, 255))  # Renderiza o número como texto
    text_rect = text.get_rect(center=(640, 100))  # Centraliza o texto na tela
    window.blit(text, text_rect) 
    
    if pause:
        draw_pause_menu(window)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        
        if pygame.sprite.collide_mask(player, obj):
            if obj.name == "sink":
                continue
            if obj.name == "fire":
                continue
            if obj.name == "table":
                continue
            if obj.name == "fridge":
                continue
            if obj.name == "door":
                continue
            if obj.name == "bush1":
                continue
            if obj.name == "bush2":
                continue
            if obj.name == "bathtub":
                continue
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

def heat_damage(player, countdown):
    from main import death
    player.god_timer = 1000
    if countdown < 175 and player.calor > 1000:
        player.make_hit()
        if player.life <= 0:
            death()


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
    from main import death

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
        if obj and obj.name == "fire":
            player.calor += 30
        if obj and obj.name == "sink":
           player.calor -= 10
        if obj and obj.name == "bathtub":
           player.calor -= 50
        if obj and obj.name == "toilet":
           player.calor -= 2
        if obj and obj.name == "fridge":
           player.calor -= 30
        if obj and obj.name == "tree":
           player.calor -= 5
        if obj and obj.name == "stove":
           player.calor += 10
        if obj and obj.name == "tree2":
           player.calor -= 2
        if obj and obj.name == "car":
           player.calor += 40
        if obj and obj.name == "tree3":
           player.calor -= 30
        
def main(window):
    from objects import Bathtub, Closet, Sink, Stove, Toilet, Table, Fridge, Tree, Fire, Bush1, Bush2, Bush3, Tree2, Car, Tree3
    from main import victory

    clock = pygame.time.Clock()
    pause = False
    block_size = 96 
    countdown = 180
    
    player = Player(450, 600, 50, 50)

    bathtub = Bathtub(1100, HEIGHT - 810    , 200)
    closet_size = 110
    closet = Closet(1300, HEIGHT - closet_size * 4.6 - 58, 200)
    sink_size = 80
    sink = Sink(2200, HEIGHT - sink_size * 9.3 - 58, 200)
    stove_size = 145
    stove = Stove(2200, HEIGHT - stove_size, 200)
    toilet_size = 80
    toilet = Toilet(1400, HEIGHT - toilet_size * 9.3 - 58, 200)
    table_size = 80
    table = Table(1200, HEIGHT - table_size * 2.02 - 58, 200)
    fridge = Fridge(2000, HEIGHT - 240, 500)
    bush3 = Bush3(140, HEIGHT - 230, 500)
    bush1 = Bush1(350, HEIGHT - 155, 500)
    bush2 = Bush2(600, HEIGHT - 205, 500)
    fire = Fire(1250, HEIGHT - block_size - 130, 16, 32)
    fire.on()

    # esse for de cima vai colocar mais blocos no chão
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range((-WIDTH * 2) // block_size, (WIDTH * 2) // block_size)]

    # um desses aqui coloca blocos na tela
    objects = [*floor,
               #    distancia X altura
               closet,
               bathtub,
               sink,
               stove,
               toilet,table, fridge, fire, bush1, bush2, bush3,
               Wood(block_size * 10, HEIGHT - block_size * 3, block_size),
               Wood(block_size * 10, HEIGHT - block_size * 4, block_size),
               Wood(block_size * 10, HEIGHT - block_size * 5, block_size),
               Wood(block_size * 10, HEIGHT - block_size * 6, block_size),
               Wood(block_size * 10, HEIGHT - block_size * 7, block_size),
               Wood(block_size * 10, HEIGHT - block_size * 8, block_size),
               Wood(block_size * 10, HEIGHT - block_size * 9, block_size),
               Wood(block_size * 10, HEIGHT - block_size * 10, block_size),
               Wood(block_size * 11, HEIGHT - block_size * 10, block_size),
               Wood(block_size * 11, HEIGHT - block_size * 11, block_size),
               Wood(block_size * 12, HEIGHT - block_size * 11, block_size),
               Wood(block_size * 12, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 13, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 3, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 4, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 5, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 6, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 2, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 7, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 8, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 9, block_size),
               Wood(block_size * 25, HEIGHT - block_size * 10, block_size),
               Wood(block_size * 24, HEIGHT - block_size * 10, block_size),
               Wood(block_size * 24, HEIGHT - block_size * 11, block_size),
               Wood(block_size * 23, HEIGHT - block_size * 11, block_size),
               Wood(block_size * 23, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 22, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 21, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 20, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 19, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 18, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 17, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 16, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 15, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 14, HEIGHT - block_size * 12, block_size),
               Wood(block_size * 11, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 11.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 12, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 12.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 13, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 13.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 14, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 14.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 15, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 15.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 16, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 16.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 17, HEIGHT - \
                     block_size * 4, block_size/2), 
               Wood(block_size * 17.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 18, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 18.5, HEIGHT - \
                     block_size * 2.5, block_size/2),
               Wood(block_size * 19, HEIGHT - block_size * 3, block_size/2),
               Wood(block_size * 19.5, HEIGHT - \
                     block_size * 3.5, block_size/2),
               Wood(block_size * 20, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 20.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 21, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 21.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 22, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 22.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 23, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 23.5, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 24, HEIGHT - block_size * 4, block_size/2),
               Wood(block_size * 24.5, HEIGHT - block_size * 4, block_size/2),

               Wood(block_size * 11, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 11.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 12, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 12.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 13, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 13.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 14, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 14.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 15, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 15.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 16, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 16.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 17, HEIGHT - \
                     block_size * 7, block_size/2),
               Wood(block_size * 17.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 18, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 18.5, HEIGHT - \
                     block_size * 6.5, block_size/2),
               Wood(block_size * 19, HEIGHT - block_size * 6, block_size/2),
               Wood(block_size * 19.5, HEIGHT - \
                     block_size * 5.5, block_size/2),
               Wood(block_size * 20, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 20.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 21, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 21.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 22, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 22.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 23, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 23.5, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 24, HEIGHT - block_size * 7, block_size/2),
               Wood(block_size * 24.5, HEIGHT - block_size * 7, block_size/2),
               Tree(-200, HEIGHT - 594, 500),
                Tree2(-900, HEIGHT - 540, 500),
                Car( -1600, HEIGHT - 600, 500),
                Tree3( -2400, HEIGHT - 515, 500),

                Wood(-(block_size * 24), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 25), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 23), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 26), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 27), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 22), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 22), HEIGHT - block_size * 8, block_size),
                Wood(-(block_size * 22), HEIGHT - block_size * 9, block_size),
                Wood(-(block_size * 22), HEIGHT - block_size * 10, block_size),
                Wood(-(block_size * 28), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 28), HEIGHT - block_size * 6, block_size),
                Wood(-(block_size * 28), HEIGHT - block_size * 7, block_size),
                Wood(-(block_size * 28), HEIGHT - block_size * 8, block_size),
                Wood(-(block_size * 28), HEIGHT - block_size * 9, block_size),
                Wood(-(block_size * 28), HEIGHT - block_size * 10, block_size),
                Wood(-(block_size * 27), HEIGHT - block_size * 10, block_size),
                Wood(-(block_size * 26), HEIGHT - block_size * 10, block_size),
                Wood(-(block_size * 24), HEIGHT - block_size * 5, block_size),
                Wood(-(block_size * 23), HEIGHT - block_size * 5, block_size),
                
                Wood(-(block_size * 22.5), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 23), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 23.5), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 24), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 24.5), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 25), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 25.5), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 26), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 26.5), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 27), HEIGHT - block_size * 5, block_size/2),
                Wood(-(block_size * 27.5), HEIGHT - block_size * 5, block_size/2),



               ]

    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 75                         
    
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
                    clock.tick(0)
                        
        if pause == False:
            player.loop(FPS)
            fire.loop()
            if player.calor < 0:
                player.calor = 0
            else:
                player.calor += 1
            heat_damage(player, countdown)
            handle_move(player, objects)

        draw(window, player, objects, offset_x,  offset_y, countdown, pause)

        if pause == False:
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel
            if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or (
            (player.rect.top - offset_y <= (scroll_area_height + 100)) and player.y_vel < 0):
                offset_y += player.y_vel
            countdown -= clock.tick(FPS) / 1000
    

        if countdown <= 0:
            victory()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
