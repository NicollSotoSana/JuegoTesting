import pygame
import random
import sys
import unittest


# Dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600



class TestSpaceInvaders(unittest.TestCase):
    """Clase de prueba para el juego Space Invaders"""

    def setUp(self):
        """Configuración inicial para cada prueba"""
        pygame.init()
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Space Invaders")
        # Resto de la inicialización del juego...

    def tearDown(self):
        """Liberación de recursos después de cada prueba"""
        pygame.quit()
        sys.exit()

    def test_movimiento_jugador(self):
        """Prueba el movimiento del jugador"""
        jugador = jugador()
        jugador.rect.centerx = ANCHO // 2
        jugador.rect.bottom = ALTO - 10

        # Mover hacia la izquierda
        jugador.update(-1)
        self.assertEqual(jugador.rect.x, ANCHO // 2 + jugador.velocidad)

        # Mover hacia la derecha
        jugador.update(1)
        self.assertEqual(jugador.rect.x, ANCHO // 2)

        # No mover
        jugador.update(0)
        self.assertEqual(jugador.rect.x, ANCHO // 2)

    def test_colision_jugador_invasor(self):
        """Prueba la colisión entre el jugador y los invasores"""
        jugador = jugador()
        jugador.rect.centerx = ANCHO // 2
        jugador.rect.bottom = ALTO - 10

        invasor = invasor()
        invasor.rect.centerx = ANCHO // 2
        invasor.rect.bottom = ALTO - 10

        # Verificar que no haya colisión inicialmente
        colisiones = pygame.sprite.spritecollide(jugador, invasor, False)
        self.assertEqual(len(colisiones), 0)

        # Simular colisión
        invasor.rect.centerx = ANCHO // 2 + 5
        colisiones = pygame.sprite.spritecollide(jugador, invasor, True)
        self.assertEqual(len(colisiones), 1)
        self.assertEqual(jugador.vidas, 2)

    def test_fin_del_juego(self):
        """Prueba el fin del juego"""
        jugador = jugador()
        jugador.vidas = 1

        invasor = invasor()
        invasor.rect.centerx = ANCHO // 2
        invasor.rect.bottom = ALTO - 10

        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

            colisiones = pygame.sprite.spritecollide(jugador, invasor, True)
            if len(colisiones) > 0:
                jugador.vidas -= 1

            if jugador.vidas <= 0:
                ejecutando = False

        self.assertEqual(jugador.vidas, 0)

    def test_reinicio_invasores(self):
        """Prueba el reinicio de los invasores"""
        invasor = invasor()
        invasor.rect.x = 100
        invasor.rect.y = 100

        invasor.update()
        self.assertTrue(invasor.rect.y > ALTO + 10)
        self.assertTrue(0 <= invasor.rect.x < ANCHO - invasor.rect.width)

    def test_tiempo_transcurrido(self):
        """Prueba el tiempo transcurrido"""
        tiempo_inicial = pygame.time.get_ticks()

        # Esperar 5 segundos
        ejecutando = True
        while ejecutando:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - tiempo_inicial) // 1000

            if tiempo_transcurrido >= 5:
                ejecutando = False

        self.assertEqual(tiempo_transcurrido, 5)



if __name__ == '__main__':
    unittest.main(exit=False)
