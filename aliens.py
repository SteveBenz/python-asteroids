import random
import pygame
from pygame.event import Event
from pygame.surface import Surface
from bullet import Bullet
from MovingPoint import MovingPoint
from GameObject import MobileGameObject, AsteroidsEvent

class Alien(MobileGameObject):
    __BulletSpeed = 0.005
    __ShipSize = 0.02
    __Speed = .001

    def __init__(self, window: Surface):
        (cx,cy) = window.get_size()
        if random.random() <= .5:
            rx = random.random()*cx
            ry = 0
        else:
            ry = random.random()*cy
            rx = 0
        super().__init__(window, 'aliens', MovingPoint(rx, ry, 0, 0, (cx,cy)))
        self._debrisType = 'lines'
        speed=self._position.scale(Alien.__Speed)
        self._position.setSpeed(random.random()*360, speed)
    
    @property
    def _radius(self) -> float:
        # Note that radius is the one used for collisions - and we make the contact area just a bit smaller
        # to not enrage players because the radius doesn't conform to the triangle of the ship
        return self._position.scale(Alien.__ShipSize*.6)

    def _draw(self) -> None:
        sizeX = sizeY = self._position.scale(self._getShipSize())
        shipImage = pygame.Surface((sizeX,sizeY), pygame.SRCALPHA)
        pygame.draw.polygon(shipImage, (255,165,0),
                    [(sizeX, sizeY/3),
                    (0, sizeY/3),
                    (sizeX, sizeY/3),
                    (sizeX/3*2, 0),
                    (sizeX/3, 0),
                    (0, sizeY/3),
                    (sizeX/3, sizeY/3*2),
                    (sizeX/3*2, sizeY/3*2)], width=2)
        (sizeX, sizeY) = shipImage.get_size()
        (cx,cy) = self._position.getPosition()
        self._window.blit(shipImage, (cx - sizeX/2, cy - sizeY/2))

    def _getBulletAngle(self) -> float:
        return 0

    def _getShipSize(self) -> float:
        return 0
    
    def __shoot(self) -> None:
        b = Bullet(self._window, 'aliens', self._position.launch(self._position.scale(Alien.__BulletSpeed), self._getBulletAngle()))
        AsteroidsEvent.PostAddEvent(b)

    def __jink(self) -> None:
        speed=self._position.scale(Alien.__Speed)
        self._position.setSpeed(random.random()*360, speed)

    def update(self, events: list[Event]) -> None:
        self._position.coast()
        if random.random() <= .01:
            self.__shoot()
        if random.random() <= .005:
            self.__jink()
        super().update(events)

class BigAlien(Alien):
    def _getBulletAngle(self) -> float:
        return random.random()*360

    def _getShipSize(self) -> float:
        return .04

    def getScore(self) -> int:
        return 300

class SmallAlien(Alien):
    def _getBulletAngle(self) -> float:
        return random.random()*360

    def _getShipSize(self) -> float:
        return .02

    def getScore(self) -> int:
        return 500
