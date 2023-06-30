import pygame
import sys
import subprocess

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego con Menú")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fuente
font = pygame.font.Font(None, 36)

# Variables del menú
start_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 - 50, 190, 50)
quit_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 50, 190, 50)

# Cargar imagen de fondo del menú
background_image = pygame.image.load("fondo.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Bucle principal del juego
running = True
in_menu = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    in_menu = False
                elif quit_button.collidepoint(mouse_pos):
                    running = False

    screen.blit(background_image, (0, 0))

    if in_menu:
        #subprocess.Popen(["python", "juego.py"])
        #in_menu = False
        pygame.draw.rect(screen, BLACK, start_button)
        pygame.draw.rect(screen, BLACK, quit_button)
        start_text = font.render("Iniciar Juego", True, WHITE)
        quit_text = font.render("Cerrar Juego", True, WHITE)
        screen.blit(start_text, (start_button.x + 20, start_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 25, quit_button.y + 10))
    else:
        # Aquí puedes agregar tu lógica de juego
        game_text = font.render("¡Juego en curso!", True, BLACK)
        screen.blit(game_text, (screen_width // 2 - 100, screen_height // 2 - 50))
        subprocess.Popen(["python", "juego.py"])
        in_menu=True

    pygame.display.flip()

pygame.quit()
