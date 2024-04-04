import pygame
import sys
from button import *
import level_1 as lv1
import level_2 as lv2
import level_3 as lv3


pygame.init()

WIDTH = 1280
HEIGHT = 720

container_width = 1080
container_height = 680

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lore of the characters")

menu_bg = pygame.image.load("assets/Background/Background.gif").convert()
menu_bg = pygame.transform.scale(menu_bg, (1280, 720))

lore_screen = pygame.Surface((container_width, container_height), pygame.SRCALPHA)  
lore_screen.fill((31, 182, 214, 50))     

# Texto de lore - descrição
def text(texto):

    text = texto 

    max_line_length = 30
    text_lines = []
    current_line = ""

    for word in text.split():
        if len(current_line) + len(word) <= max_line_length:
            current_line +=word +" "
        else:
            text_lines.append(current_line)
            current_line = word +" "
    if current_line:
        text_lines.append(current_line)

    text_rendered = [get_font(30).render(line, True, (255, 255, 255)) for line in text_lines]

    text_x = 600
    text_y = 150

    # Exibe o texto renderizado na superficie lore_screen
    for line_rendered in text_rendered:
        lore_screen.blit(line_rendered, (text_x, text_y))
        # Avança pra proxima linha
        text_y += line_rendered.get_height() + 5

def get_text():
    lore_x = (WIDTH - container_width) // 2
    lore_y = (HEIGHT - container_height) // 2
    window.blit(lore_screen, (lore_x, lore_y))
    

def level_1():
    from main import level_select

    texto_1 = "Os tempos mudaram. Sofia Cinta Damai mora na Mooca e, com as mudanças climáticas, seres ancestrais despertaram. O Ciclone Katrina invadiu Brasil e está criando enchentes em São Paulo. A Única esperança de Sofia é fugir da correnteza de água, pulando por cima de carros e outros objetos para não ser pega na inundação. Seu objetivo é alcançar o barco para que sobreviva à São Paulo submerso"
    
    max_line_length = 30
    text_lines = []
    current_line = ""

    for word in texto_1.split():
        if len(current_line) + len(word) <= max_line_length:
            current_line +=word +" "
        else:
            text_lines.append(current_line)
            current_line = word +" "
    if current_line:
        text_lines.append(current_line)

    text_rendered = [get_font(30).render(line, True, (255, 255, 255)) for line in text_lines]

    text_x = 600
    text_y = 150

    # Exibe o texto renderizado na superficie lore_screen
    for line_rendered in text_rendered:
        lore_screen.blit(line_rendered, (text_x, text_y))
        # Avança pra proxima linha
        text_y += line_rendered.get_height() + 5



    personagem = "assets/MainCharacters/NinjaFrog/foto-inicial-ninja-frog.png"
    imgem_personagem = pygame.image.load(personagem).convert_alpha()
    imgem_personagem = pygame.transform.scale(
        imgem_personagem, (300, 300))
    while True:
        level_mouse_pos = pygame.mouse.get_pos()

        window.fill("white")
        level_selector_bg = pygame.image.load(
            "assets/Background/level_selector_bg.png").convert()
        level_selector_bg = pygame.transform.scale(
            level_selector_bg, (1280, 720))
        
        window.blit(level_selector_bg, (0, 0))
        window.blit(lore_screen, (100,20))
        window.blit(imgem_personagem, (150, 90))

        title_text = get_font(100).render("ENCHENTE", True, (130, 200, 150))
        title_rect = title_text.get_rect(center=(container_width-200, container_height-580))
        window.blit(title_text, title_rect)

        lore_x = (WIDTH - container_width) // 2
        lore_y = (HEIGHT - container_height) // 2
        window.blit(lore_screen, (lore_x, lore_y))
    

        play_button = Button(image=pygame.image.load("assets/ButtonStyle/Play Rect.png"), pos=(container_width-770, container_height-160),
                             text_input="Começar", font=get_font(35), base_color="White", hovering_color="Green")
        return_button = Button(image=pygame.image.load("assets/ButtonStyle/return.png"), pos=(170, 630),
                               text_input="<", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        return_button.changeColor(level_mouse_pos)
        return_button.update(window)
        play_button.changeColor(level_mouse_pos)
        play_button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(level_mouse_pos):
                    lv1.main(window)
                if return_button.checkForInput(level_mouse_pos):
                    level_select()

        pygame.display.update()


def level_2():
    from main import level_select

    texto_2 = "Os tempos mudaram. Roberto, nascido na Noruega em 2000, agora com 30 anos, enfrenta mais uma anomalia do Aquecimento Global. O Verão de Oslo está intenso e Roberto começa a não suportar mais o calor. Seu objetivo é sobreviver à onda de calor até que acabe o dia. Você precisa agir e fazer atividades que te refresquem para que não faleça de insolaçaõ"
    text(texto_2)
    personagem = "assets/MainCharacters/MaskDude/foto-inicial-mask-dude.png"
    imgem_personagem = pygame.image.load(personagem).convert_alpha()
    imgem_personagem = pygame.transform.scale(
        imgem_personagem, (300, 300))
    while True:
        level_mouse_pos = pygame.mouse.get_pos()

        
        window.fill("white")
        level_selector_bg = pygame.image.load(
            "assets/Background/level_selector_bg.png").convert()
        level_selector_bg = pygame.transform.scale(
            level_selector_bg, (1280, 720))
        
        window.blit(level_selector_bg, (0, 0))
        window.blit(lore_screen, (100,20))
        window.blit(imgem_personagem, (150, 90))

        title_text = get_font(75).render(
            "ONDA DE CALOR", True, (130, 200, 150))
        title_rect = title_text.get_rect(center=(container_width-200, container_height-580))
        window.blit(title_text, title_rect)

        get_text()

        play_button = Button(image=pygame.image.load("assets/ButtonStyle/Play Rect.png"), pos=(container_width-770, container_height-160),
                             text_input="Começar", font=get_font(35), base_color="White", hovering_color="Green")
        return_button = Button(image=pygame.image.load("assets/ButtonStyle/return.png"), pos=(170, 630),
                               text_input="<", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        return_button.changeColor(level_mouse_pos)
        return_button.update(window)
        play_button.changeColor(level_mouse_pos)
        play_button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(level_mouse_pos):
                    lv2.main(window)
                if return_button.checkForInput(level_mouse_pos):
                    level_select()

        pygame.display.update()


def level_3():
    from main import level_select

    texto_3 = " Os tempos mudaram. Cezar está em uma expedição na Antártida em busca de recursos novos que descongelaram com o aquecimento global. Mas, um passo em falso, despertaram O Avalanche, devido ao derretimento das montanhas de gelo. Seu objetivo é encontrar maneiras de sobreviver às ondas inacabáveis de gelo escorrendo pela montanha e alcançar o ponto de fuga."
    text(texto_3)
    personagem = "assets/MainCharacters/VirtualGuy/foto-inicial-virtual-guy.png"
    imgem_personagem= pygame.image.load(personagem).convert_alpha()
    imgem_personagem = pygame.transform.scale(
        imgem_personagem, (300, 300))

    while True:
        level_mouse_pos = pygame.mouse.get_pos()

        window.fill("white")
        level_selector_bg = pygame.image.load(
            "assets/Background/level_selector_bg.png").convert()
        level_selector_bg = pygame.transform.scale(
            level_selector_bg, (1280, 720))
        
        window.blit(level_selector_bg, (0, 0))
        window.blit(lore_screen, (100,20))
        window.blit(imgem_personagem, (150, 90))

        title_text = get_font(100).render("Avalanche", True, (130, 200, 150))
        title_rect = title_text.get_rect(center=(container_width-200, container_height-580))
        window.blit(title_text, title_rect)

        get_text()

        play_button = Button(image=pygame.image.load("assets/ButtonStyle/Play Rect.png"), pos=(container_width-770, container_height-160),
                             text_input="Começar", font=get_font(35), base_color="White", hovering_color="Green")
        return_button = Button(image=pygame.image.load("assets/ButtonStyle/return.png"), pos=(170, 630),
                               text_input="<", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        return_button.changeColor(level_mouse_pos)
        return_button.update(window)
        play_button.changeColor(level_mouse_pos)
        play_button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(level_mouse_pos):
                    lv3.main(window)
                if return_button.checkForInput(level_mouse_pos):
                    level_select()

        pygame.display.update()
