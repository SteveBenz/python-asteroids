import pygame
from pygame.event import Event
from pygame.surface import Surface
from bullet import Bullet
from MovingPoint import MovingPoint, ScreenSize
import userEvents

class Ship:
    __AccelerationRate = .00002
    __TurnRate = 2
    __BulletSpeed = .005

    def __init__(self, window: Surface):
        (cx,cy) = window.get_size()
        self.__position = MovingPoint(cx/2, cy/2, 0, 0, (cx,cy))

        self.__window = window
        self.__direction = 0
        self.__isTurningCcw = False
        self.__isTurningCw = False
        self.__isAccelerating = False

    def __draw(self) -> None:
        # pygame.draw.circle(ballImage, Drawing.BallColors[i], [x,y], Drawing.CircleRadius)
        sizeX = sizeY = self.__position.scale(0.02)
        shipImage = pygame.Surface((sizeX,sizeY), pygame.SRCALPHA)
        pygame.draw.polygon(shipImage, (255,255,255),
                    [(sizeX, sizeY/2),
                    (0, sizeY/6),
                    (sizeX/10, sizeY/2),
                    (0, 5*sizeY/6)], width=2)
        shipImage = pygame.transform.rotate(shipImage, self.__direction)
        (sizeX, sizeY) = shipImage.get_size()
        (cx,cy) = self.__position.getPosition()
        self.__window.blit(shipImage, (cx - sizeX/2, cy - sizeY/2))
    
    def __shoot(self) -> None:
        b = Bullet(self.__window, self.__position.launch(self.__position.scale(Ship.__BulletSpeed), self.__direction))
        pygame.event.post(Event(userEvents.BULLET, **{'bullet': b, 'action': 'add' }))

    def update(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.__isAccelerating = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_w:
                self.__isAccelerating = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.__isTurningCcw = True
                self.__isTurningCw = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_a:
                self.__isTurningCcw = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.__isTurningCw = True
                self.__isTurningCcw = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                self.__isTurningCw = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__shoot()

        if self.__isAccelerating:
            self.__position.accelerate(self.__position.scale(Ship.__AccelerationRate), self.__direction)
        if self.__isTurningCcw:
            self.__direction += Ship.__TurnRate
        if self.__isTurningCw:
            self.__direction -= Ship.__TurnRate
        self.__position.coast()
        self.__draw()

    def handleResize(self, size: ScreenSize) -> None:
        self.__position.handleResize(size)