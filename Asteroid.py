from __future__ import annotations
import math
import pygame
import random
from pygame.event import Event
from pygame.surface import Surface
from MovingPoint import MovingPoint
from GameObject import GameObject, MobileGameObject, AsteroidsEvent

class Asteroid(MobileGameObject):
    __StartSize = .01
    __StartSpeed = .0002
    __BreakSpeed = .0001

    def __init__(self, window: Surface, startSize: int, position: MovingPoint):
        super().__init__(window, 'asteroids', position)
        self.__size = startSize

    @property
    def _radius(self) -> float:
        return self._position.scale(self.__size * Asteroid.__StartSize)

    def _draw(self) -> None:
        pygame.draw.circle(self._window, (128,128,128), self._position.getPosition(), self._radius, 2)
    
    def getScore(self) -> int:
         return self.__size*15


    def update(self, events: list[Event]) -> None:
        super().update(events)

    def handleCollision(self, impactedWith: GameObject) -> None:
        super().handleCollision(impactedWith)
        if self.__size > 1:
            direction = random.random()*180
            speed = self._position.scale(Asteroid.__BreakSpeed)
            m1 = self._position.launch(speed, direction)
            m2 = self._position.launch(speed, direction+180)
            newSize = self.__size // 2
            AsteroidsEvent.PostAddEvent(Asteroid(self._window, newSize, m1))
            AsteroidsEvent.PostAddEvent(Asteroid(self._window, newSize, m2))    

    @staticmethod
    def CreateStartAsteroid(window: Surface) -> Asteroid:
        (cx,cy) = window.get_size()
        startSize = 4
        size = min(cx, cy) * Asteroid.__StartSize * startSize

        startSide = random.choice(['left', 'right', 'top', 'bottom'])
        if startSide == 'left':
            x = -size
            y = random.randint(0, cy)
            if y < cy/2:
                direction = -random.random()*80
            else:
                direction = random.random()*80
        elif startSide == 'right':
            x = cx+size
            y = random.randint(0, cy)
            if y < cy/2:
                direction = 180+random.random()*80
            else:
                direction = 180-random.random()*80
        elif startSide == 'top':
            x = random.randint(0, cx)
            y = -size
            if x < cx/2:
                direction = -(10+random.random()*80)
            else:
                direction = 180+(10+random.random()*80)
        else:
            x = random.randint(0,cx)
            y = cy+size
            if x < cx/2:
                direction = 10+random.random()*80
            else:
                direction = 180-(10+random.random()*80)
        
        dx = Asteroid.__StartSpeed*cx*math.cos(math.radians(direction))
        dy = -Asteroid.__StartSpeed*cy*math.sin(math.radians(direction))
        return Asteroid(window, startSize, MovingPoint(x, y, dx, dy, (cx,cy)))
