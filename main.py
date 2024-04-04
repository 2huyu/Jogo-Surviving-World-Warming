import pygame
import sys
from button import *
from level_lore import *
from sys import argv
import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

menu_bg = pygame.image.load("assets/Background/Background.gif").convert()
menu_bg = pygame.transform.scale(menu_bg, (1280, 720))


def get_font(size):
    return pygame.font.Font("assets/Font/FantaisieArtistique.ttf", size)


def get_font_title(size):
    return pygame.font.Font("assets/Font/Humanistic.ttf", size)


def death():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("white")

        OPTIONS_TEXT = get_font(45).render("Você perdeu.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def victory():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("white")

        OPTIONS_TEXT = get_font(45).render("Parabéns! Você aprendeu a sobreviver", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        window.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="Voltar", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def aprenda():
    texto_aprenda = "Este jogo visa ensinar o jogador a sobreviver em ambientes simulados de desastres naturais provocados pelo Aquecimento Global"
    text(texto_aprenda)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("white")

        get_text()

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def level_select():
    while True:
        level_mouse_pos = pygame.mouse.get_pos()

        window.fill("white")
        level_selector_bg = pygame.image.load(
            "assets/Background/level_selector_bg.png").convert()
        level_selector_bg = pygame.transform.scale(
            level_selector_bg, (1280, 720))
        window.blit(level_selector_bg, (0, 0))

        title_text = get_font_title(100).render(
            "Surviving World Warming", True, (130, 200, 150))
        title_rect = title_text.get_rect(center=(640, 100))
        window.blit(title_text, title_rect)

        return_button = Button(image=pygame.image.load("assets/ButtonStyle/return.png"), pos=(100, 650),
                               text_input="<", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        level_1_button = Button(image=pygame.image.load("assets/ButtonStyle/Play Rect.png"), pos=(640, 250),
                                text_input="Nível 1", font=get_font(75), base_color="White", hovering_color="Green")
        level_2_button = Button(image=pygame.image.load("assets/ButtonStyle/Play Rect.png"), pos=(640, 400),
                                text_input="Nível 2", font=get_font(75), base_color="White", hovering_color="Green")
        level_3_button = Button(image=pygame.image.load("assets/ButtonStyle/Play Rect.png"), pos=(640, 550),
                                text_input="Nível 3", font=get_font(75), base_color="White", hovering_color="Green")

        for i in [level_1_button, level_2_button, level_3_button, return_button]:
            i.changeColor(level_mouse_pos)
            i.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_1_button.checkForInput(level_mouse_pos):
                    level_1()
                if level_2_button.checkForInput(level_mouse_pos):
                    level_2()
                if level_3_button.checkForInput(level_mouse_pos):
                    level_3()
                if return_button.checkForInput(level_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():

    while True:

        window.blit(menu_bg, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font_title(100).render(
            "Surviving World Warming", True, "#ff9966")
        menu_rect = menu_text.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/ButtonStyle/Play Rect.png"), pos=(640, 250),
                             text_input="JOGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/ButtonStyle/Options Rect.png"), pos=(640, 400),
                                text_input="APRENDA", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/ButtonStyle/Quit Rect.png"), pos=(640, 550),
                             text_input="SAIR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        window.blit(menu_text, menu_rect)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                    level_select()
                if OPTIONS_BUTTON.checkForInput(menu_mouse_pos):
                    aprenda()
                if QUIT_BUTTON.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
