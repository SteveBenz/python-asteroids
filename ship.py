import pygame
from pygame.event import Event
from pygame.surface import Surface
from bullet import Bullet, BulletEvent
from coordinateSpace import Velocity
from coordinateSpace import GamePoint, mapPoint

class Ship:
    __AccelerationRate = .00002
    __TurnRate = 2
    __BulletSpeed = .05

    def __init__(self, window: Surface):
        self.velocity: Velocity = Velocity()
        self.position: GamePoint = (.5,.5)

        self.__window = window
        self.__direction = 0
        self.__isTurningCcw = False
        self.__isTurningCw = False
        self.__isAccelerating = False

    def __draw(self) -> None:
        # pygame.draw.circle(ballImage, Drawing.BallColors[i], [x,y], Drawing.CircleRadius)
        (sizeX, sizeY) = mapPoint((.02,.02), self.__window)
        shipImage = pygame.Surface((sizeX, sizeY), pygame.SRCALPHA)
        pygame.draw.polygon(shipImage, (255,255,255),
                    [(sizeX, sizeY/2),
                    (0, sizeY/6),
                    (sizeX/10, sizeY/2),
                    (0, 5*sizeY/6)], width=2)
        shipImage = pygame.transform.rotate(shipImage, self.__direction)
        (sizeX, sizeY) = shipImage.get_size()

        (cx, cy) = mapPoint(self.position, self.__window)
        self.__window.blit(shipImage, (cx - sizeX/2, cy - sizeY/2))
    
    def __shoot(self) -> None:
        b = Bullet(self.__window, self.position, self.velocity.accelerate(Ship.__BulletSpeed, self.__direction))
        pygame.event.post(BulletEvent(b, 'add'))

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
            self.velocity = self.velocity.accelerate(Ship.__AccelerationRate, self.__direction)
        if self.__isTurningCcw:
            self.__direction += Ship.__TurnRate
        if self.__isTurningCw:
            self.__direction -= Ship.__TurnRate
        self.position = self.velocity.move(self.position)
        self.__draw()
