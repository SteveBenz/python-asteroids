from abc import abstractmethod
import random
import pygame
from pygame.event import Event
from pygame.surface import Surface
from Tweakables import Balance, Colors, Scoring, Sizes
from bullet import Bullet
from MovingPoint import MovingPoint
from GameObject import MobileGameObject, AsteroidsEvent

class Alien(MobileGameObject):

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
        speed=self._position.scale(Balance.ALIEN_SPEED)
        self._position.setSpeed(random.random()*360, speed)
    
    def _draw(self) -> None:
        sizeX = sizeY = self._radius*2
        shipImage = pygame.Surface((sizeX,sizeY), pygame.SRCALPHA)
        pygame.draw.polygon(shipImage, Colors.ALIEN_SHIP,
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

    @abstractmethod
    def _getBulletAngle(self) -> float:
        pass

    @abstractmethod
    def _getShipSize(self) -> float:
        pass
    
    def __shoot(self) -> None:
        b = Bullet(self._window, 'aliens', self._position.launch(self._position.scale(Balance.ALIEN_BULLET_SPEED), self._getBulletAngle()))
        AsteroidsEvent.PostAddEvent(b)

    def __jink(self) -> None:
        speed=self._position.scale(Balance.ALIEN_SPEED)
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

    @property
    def _radius(self) -> float:
        return self._position.scale(Sizes.BIG_ALIEN)/2

    def getScore(self) -> int:
        return Scoring.BIG_ALIEN

class SmallAlien(Alien):
    def _getBulletAngle(self) -> float:
        return random.random()*360

    @property
    def _radius(self) -> float:
        return self._position.scale(Sizes.SMALL_ALIEN)/2

    def getScore(self) -> int:
        return Scoring.SMALL_ALIEN
