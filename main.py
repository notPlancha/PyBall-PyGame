import sys

import pygame
from pygame import constants as pygameEnum
import Player as Ps
from Colors import Colors
from utils import module
pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1344, 756
screen = pygame.display.set_mode((width, height))

centerX, centerY = int(width / 2), int(height / 2)

fpsCount = 0

Players = Ps.PlayerList(Ps.Player(
    horizMovement=Ps.Movement(
        posKey=Ps.PlayerKey(pygameEnum.K_RIGHT),
        negKey=Ps.PlayerKey(pygameEnum.K_LEFT)
    ),
    vertiMovement=Ps.Movement(
        posKey=Ps.PlayerKey(pygameEnum.K_DOWN),
        negKey=Ps.PlayerKey(pygameEnum.K_UP)
    ),
    color=Colors.RED.value,
    pos=[centerX, centerY],
    radius=50
))
while True:
    fpsCount += 1
    screen.fill(Colors.BLACK.value)
    # events
    for event in pygame.event.get():
        if event.type == pygameEnum.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygameEnum.KEYDOWN:
            Players.handleKeyDown(event.key)
        if event.type == pygameEnum.KEYUP:
            Players.handleKeyUp(event.key)

    # players
    for P in Players:
        if P.isVisible:
            # check if keys are pressed and handle it
            for MP in [P.horizMovement, P.vertiMovement]:
                if MP.posKey.isKeyPressed:
                    MP.speed += MP.acelaration
                if MP.negKey.isKeyPressed:
                    MP.speed -= MP.acelaration
                # apply friction
                if MP.speed < 0:
                    MP.speed += MP.Friction
                    if MP.speed > 0:
                        MP.speed = 0
                else:
                    MP.speed -= MP.Friction
                    if MP.speed < 0:
                        MP.speed = 0
            # change pos based on speed
            P.pos[0] += P.horizMovement.speed
            P.pos[1] += P.vertiMovement.speed
            # draw circle
            pygame.draw.circle(screen, P.color, (int(P.pos[0]), int(P.pos[1])), P.radius, P.thickness)

    # game update
    pygame.display.flip()
    fpsClock.tick(fps)
