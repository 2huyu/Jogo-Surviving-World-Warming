import pygame
import sys
from button import *


def draw_pause_menu(window):
    from main import main_menu
    

    mouse_posicao = pygame.mouse.get_pos()
    pause_rect = pygame.Surface((400,600), pygame.SRCALPHA)  
    pause_rect.fill((200, 200, 200, 150))
    window.blit(pause_rect, (450, 100))
    pause_text = get_font(20).render("Jogo Pausado", True, "Black")
    text_rect = pause_text.get_rect(center=(640, 260))
    window.blit(pause_text, text_rect)

    opcao_menu = Button(image=None, pos=(640, 550), 
                        text_input="SAIR", font=get_font(75), base_color="Black", hovering_color="Green")
    opcao_continuar = Button(image=None, pos=(640, 400), 
                        text_input="Aperte ESC para continuar", font=get_font(30), base_color="Black", hovering_color="Black")

    opcao_menu.changeColor(mouse_posicao)
    opcao_continuar.changeColor(mouse_posicao)
    opcao_menu.update(window)
    opcao_continuar.update(window)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if opcao_menu.checkForInput(mouse_posicao):
                    main_menu()

    pygame.display.update()