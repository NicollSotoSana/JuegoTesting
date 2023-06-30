import pygame
import random
import sys

# Dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Inicialización de Pygame
pygame.init()

# Creación de la ventana del juego
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")

# Cargar imágenes
jugador_imagen = pygame.image.load("jugador.png").convert_alpha()
jugador_imagen = pygame.transform.scale(jugador_imagen, (50, 50))
invasor_imagen = pygame.image.load("invasor.png").convert_alpha()
explosion_imagen = pygame.image.load("explosion.png").convert_alpha()
explosion_imagen = pygame.transform.scale(explosion_imagen, (30, 30))

# Cargar sonidos
pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.set_volume(1)
colision_sonido = pygame.mixer.Sound("colision.wav")

# Clase para representar la nave espacial del jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = jugador_imagen
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad = 5
        self.vidas = 3

    def update(self, mov_x):
        self.rect.x += mov_x * self.velocidad
        self.limitar_movimiento()

    def limitar_movimiento(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ANCHO:
            self.rect.right = ANCHO

# Clase para representar los invasores alienígenas
class Invasor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = invasor_imagen
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO + 10:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randrange(1, 4)

# Clase para representar las explosiones
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = explosion_imagen
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.animacion_delay = 10
        self.animacion_contador = 0
        self.animacion_completa = False

    def update(self):
        self.animacion_contador += 1
        if self.animacion_contador >= self.animacion_delay:
            self.animacion_contador = 0
            self.animacion_completa = True

# Creación del jugador
jugador = Jugador()

# Creación de los grupos de sprites
todos_los_sprites = pygame.sprite.Group()
invasores = pygame.sprite.Group()
explosiones = pygame.sprite.Group()

# Agregar el jugador al grupo de sprites
todos_los_sprites.add(jugador)

# Creación de los invasores
for _ in range(10):
    invasor = Invasor()
    todos_los_sprites.add(invasor)
    invasores.add(invasor)

# Reloj para controlar la velocidad de actualización del juego
reloj = pygame.time.Clock()

# Variables de tiempo
tiempo_inicial = pygame.time.get_ticks()
tiempo_actual = 0
tiempo_transcurrido = 0

# Variables de juego
vidas = 3

# Reproducir música de fondo
pygame.mixer.music.play(1)

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Obtener las teclas presionadas
    teclas = pygame.key.get_pressed()

    # Movimiento del jugador
    mov_x = teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]

    # Actualizar el jugador
    jugador.update(mov_x)

    # Actualizar los invasores
    invasores.update()

    # Verificar colisiones entre los invasores y el jugador
    colisiones = pygame.sprite.spritecollide(jugador, invasores, True)
    for colision in colisiones:
        explosion = Explosion(colision.rect.centerx, colision.rect.centery)
        todos_los_sprites.add(explosion)
        explosiones.add(explosion)
        colision_sonido.play()
        vidas -= 1

    # Actualizar las explosiones
    explosiones.update()
    for explosion in explosiones:
        if explosion.animacion_completa:
            explosiones.remove(explosion)
            todos_los_sprites.remove(explosion)

    # Renderizar el juego
    ventana.fill(BLANCO)
    todos_los_sprites.draw(ventana)

    # Medidor de tiempo
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = (tiempo_actual - tiempo_inicial) // 1000

    # Mostrar vidas restantes
    fuente = pygame.font.Font(None, 36)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, NEGRO)
    ventana.blit(texto_vidas, (10, 10))

    # Mostrar tiempo transcurrido
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_transcurrido} segundos", True, NEGRO)
    ventana.blit(texto_tiempo, (10, 50))

    pygame.display.flip()
    reloj.tick(60)

    # Verificar fin del juego
    if vidas <= 0:
        ejecutando = False

# Salir del juego
pygame.quit()
sys.exit()
