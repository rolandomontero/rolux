import pygame
from pygame.locals import *
import os
import sys

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

ACTUAL_DIR = os.path.split(os.path.abspath(__file__))[0]
IMG_DIR = 'imagenes'
SONIDO_DIR = 'sonidos'

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):

    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(ACTUAL_DIR, dir_imagen, nombre)

    try:
        image = pygame.image.load(ruta)
    except:
        print ("Error, no se puede cargar la imagen: ", ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except pygame.error:
        print ("No se pudo cargar el sonido:", ruta)
        sonido = None
    return sonido

# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:


class Pelota(pygame.sprite.Sprite):
    "La bola y su comportamiento en la pantalla"

    def __init__(self, sonido_golpe, sonido_punto):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [2, 3]
        self.sonido_golpe = sonido_golpe
        self.sonido_punto = sonido_punto

    def update(self):
        if self.rect.right < 10 or self.rect.left >(SCREEN_WIDTH -10):
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
            self.sonido_punto.play()  # Reproducir sonido de punto
            self.rect.centerx = SCREEN_WIDTH / 2
            self.rect.centery = SCREEN_HEIGHT / 2
        
        self.rect.move_ip((self.speed[0], self.speed[1]))

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            self.speed[1] = -self.speed[1]
            self.sonido_golpe.play()  # Reproducir sonido de rebote


class Paleta(pygame.sprite.Sprite):
    "Define el comportamiento de las paletas de ambos jugadores"

    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = SCREEN_WIDTH / 2

    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0
  #Funciona?
    def cpu(self, pelota):
        self.speed = [2.5, 0]
        if pelota.speed[1] >= 0 and pelota.rect.centery >= SCREEN_HEIGHT / 2:
            if self.rect.centerx > pelota.rect.centerx:
                self.rect.centerx -= self.speed[0]
            if self.rect.centerx < pelota.rect.centerx:
                self.rect.centerx += self.speed[0]


# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    pygame.init()
    pygame.mixer.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ejemplo de un Pong Simple")

    # cargamos los objetos
    fondo = load_image("fondo.jpg", IMG_DIR, alpha=False)
    sonido_golpe = load_sound("tennis.ogg", SONIDO_DIR)
    sonido_punto = load_sound("aplausos.ogg", SONIDO_DIR)

    bola = Pelota(sonido_golpe, sonido_punto)
    jugador1 = Paleta(8)
  ######### Cambia la posicion SCREEN_HEIGHT no SCREEN_WIDTH ###
    jugador2 = Paleta(SCREEN_HEIGHT - 8)

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)

    # el bucle principal del juego
    going = True
    while going:
        clock.tick(60)

        # Actualizamos los obejos en pantalla
        jugador1.humano()
        jugador2.cpu(bola)
        bola.update()

        # Comprobamos si colisionan los objetos
        bola.colision(jugador1)
        bola.colision(jugador2)

        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                going = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jugador1.rect.centerx -= 5
                elif event.key == pygame.K_RIGHT:
                    jugador1.rect.centerx += 5
                elif event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                  


        # actualizamos la pantalla
        screen.blit(fondo, (0, 0))
        todos = pygame.sprite.RenderPlain(bola, jugador1, jugador2)
        todos.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
