import pygame, random, sys
from pygame.locals import *

ANCHOVENTANA = 1200
ALTOVENTANA = 600
COLORVENTANA = (255, 255, 0)
COLORTEXTO = (255, 0, 0)
COLORFONDO = (0)
FPS = 40
TAMAÑOMINMETEORITO = 10
TAMAÑOMAXMETEORITO = 40
TAMAÑOMINNUBE = 120
TAMAÑOMAXNUBE = 200
VELOCIDADMINMETEORITO = 1
VELOCIDADMAXMETEORITO = 8
VELOCIDADMINNUBE = 1
VELOCIDADMAXNUBE = 3
TASANUEVOMETEORITO = 6
TASANUEVONUBE= 25
TASAMOVIMIENTOJUGADOR = 5

def terminar():
  pygame.quit()
  sys.exit()

def esperarTeclaJugador():
  while True:
    for evento in pygame.event.get():
      if evento.type == QUIT:
        terminar()
      if evento.type == KEYDOWN:
        if evento.key == K_ESCAPE:
          terminar()
        return

def jugadorGolpeaMeteorito(rectanguloJugador, meteoritos):
  for v in meteoritos:
    if rectanguloJugador.colliderect(v['rect']):
      return True
  return False

def dibujarTexto(texto, font, superficie, x, y):
  objetotexto = font.render(texto, 1, COLORTEXTO)
  rectangulotexto = objetotexto.get_rect()
  rectangulotexto.topleft = (x, y)
  superficie.blit(objetotexto, rectangulotexto)

pygame.init()
relojPrincipal = pygame.time.Clock()
superficieVentana = pygame.display.set_mode((ANCHOVENTANA, ALTOVENTANA))
pygame.display.set_caption('Impact On Space - Héctor Cazalla')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont('ocraextended', 48)

gameOverSound = pygame.mixer.Sound('gameover-Impact On Space.wav')
pygame.mixer.music.load('bandasonora-Impact On Space.mp3')

playerImage = pygame.image.load('nave-Impact On Space.png')
rectanguloJugador = playerImage.get_rect()
baddieImage = pygame.image.load('meteorito-Impact On Space.png')
nubeImage = pygame.image.load('nebulas-Impact On Space.png')


dibujarTexto('IMPACT ON SPACE', font, superficieVentana, (ANCHOVENTANA / 2.5) -75, (ALTOVENTANA / 2.5))
dibujarTexto('Presione una tecla para comenzar', font, superficieVentana, (ANCHOVENTANA / 2.5) - 325, (ALTOVENTANA / 2.5) + 120)
pygame.display.update()
esperarTeclaJugador()

puntajeMax = 0
while True:
  meteoritos = []
  nubes = [] 
  puntaje = 0
  rectanguloJugador.topleft = (ANCHOVENTANA / 2, ALTOVENTANA - 50)
  moverIzquierda = moverDerecha = moverArriba = moverAbajo = False
  trucoReversa = trucoLento = False
  contadorAgregarMeteorito = 0
  contadorAgregarNube = 0
  pygame.mixer.music.play(-1, 0.0)

  while True:
    puntaje += 1

    for evento in pygame.event.get():
      if evento.type == QUIT:
        terminar()

      if evento.type == KEYDOWN:
        if evento.key == ord('z'):
          trucoReversa = True
        if evento.key == ord('x'):
          trucoLento = True
        if evento.key == K_LEFT or evento.key == ord('a'):
          moverDerecha = False
          moverIzquierda = True
        if evento.key == K_RIGHT or evento.key == ord('d'):
          moverIzquierda = False
          moverDerecha = True
        if evento.key == K_UP or evento.key == ord('w'):
          moverAbajo = False
          moverArriba = True
        if evento.key == K_DOWN or evento.key == ord('s'):
          moverArriba = False
          moverAbajo = True

      if evento.type == KEYUP:
        if evento.key == ord('z'):
          trucoReversa = False
          puntaje = 0
        if evento.key == ord('x'):
          trucoLento = False
          puntaje = 0
        if evento.key == K_ESCAPE:
          terminar()

        if evento.key == K_LEFT or evento.key == ord('a'):
         moverIzquierda = False
        if evento.key == K_RIGHT or evento.key == ord('d'):
         moverDerecha = False
        if evento.key == K_UP or evento.key == ord('w'):
         moverArriba = False
        if evento.key == K_DOWN or evento.key == ord('s'):
         moverAbajo = False

      if evento.type == MOUSEMOTION:
         rectanguloJugador.move_ip(evento.pos[0] - rectanguloJugador.centerx, evento.pos[1] - rectanguloJugador.centery)

    if not trucoReversa and not trucoLento:
      contadorAgregarMeteorito += 1
    if contadorAgregarMeteorito == TASANUEVOMETEORITO:
      contadorAgregarMeteorito = 0
      baddieSize = random.randint(TAMAÑOMINMETEORITO, TAMAÑOMAXMETEORITO)
      newBaddie = {'rect': pygame.Rect(random.randint(0, ANCHOVENTANA-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
      'speed': random.randint(VELOCIDADMINMETEORITO, VELOCIDADMAXMETEORITO),
      'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
      }

      meteoritos.append(newBaddie)

    if not trucoReversa and not trucoLento:
      contadorAgregarNube += 1 
    if contadorAgregarNube == TASANUEVONUBE:
      contadorAgregarNube = 0
      baddieSize1 = random.randint(TAMAÑOMINNUBE, TAMAÑOMAXNUBE)
      newBaddie1 = {'rect': pygame.Rect(random.randint(0, ANCHOVENTANA-baddieSize1), 0 - baddieSize1, baddieSize1, baddieSize1),
      'speed': random.randint(VELOCIDADMINNUBE, VELOCIDADMAXNUBE),
      'surface':pygame.transform.scale(nubeImage, (baddieSize1, baddieSize1)),
      }
      nubes.append(newBaddie1)

    if moverIzquierda and rectanguloJugador.left  > 0:
      rectanguloJugador.move_ip(-1 * TASAMOVIMIENTOJUGADOR, 0)
    if moverDerecha and rectanguloJugador.right < ANCHOVENTANA:
      rectanguloJugador.move_ip(TASAMOVIMIENTOJUGADOR, 0)
    if moverArriba and rectanguloJugador.top  > 0:
      rectanguloJugador.move_ip(0, -1 * TASAMOVIMIENTOJUGADOR)
    if moverAbajo and rectanguloJugador.bottom < ALTOVENTANA:
      rectanguloJugador.move_ip(0, TASAMOVIMIENTOJUGADOR)

    pygame.mouse.set_pos(rectanguloJugador.centerx, rectanguloJugador.centery)

    for b in meteoritos:
      if not trucoReversa and not trucoLento:
        b['rect'].move_ip(0, b['speed'])
      elif trucoReversa:
        b['rect'].move_ip(0, -5)
      elif trucoLento:
        b['rect'].move_ip(0, 1)
    
    for b in nubes:
        b['rect'].move_ip(0, b['speed']) 

    
    for b in meteoritos[:]:
      if b['rect'].top > ALTOVENTANA:
        meteoritos.remove(b)

   
    for b in nubes[:]:
       if b['rect'].top > ALTOVENTANA:
          nubes.remove(b) 

    superficieVentana.fill(COLORFONDO)

    dibujarTexto('Puntos: %s' % (puntaje), font, superficieVentana, 10, 0)
    dibujarTexto('Records: %s' % (puntajeMax), font, superficieVentana, 10, 40)

    superficieVentana.blit(playerImage, rectanguloJugador)

    for b in meteoritos:
      superficieVentana.blit(b['surface'], b['rect'])

    for b in nubes:
      superficieVentana.blit(b['surface'], b['rect']) 
    pygame.display.update()

    if jugadorGolpeaMeteorito(rectanguloJugador, meteoritos):
      if puntaje > puntajeMax:
        puntajeMax = puntaje
      break

    relojPrincipal.tick(FPS)

  pygame.mixer.music.stop()
  gameOverSound.play()

  dibujarTexto('GAME OVER', font, superficieVentana, (ANCHOVENTANA / 2.5) + 0, (ALTOVENTANA / 2.5))
  dibujarTexto('Presione una tecla para repetir', font, superficieVentana, (ANCHOVENTANA / 2.5) - 300, (ALTOVENTANA / 2.5) + 120)
  pygame.display.update()
  esperarTeclaJugador()

  gameOverSound.stop()