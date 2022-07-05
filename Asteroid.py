from __future__ import annotations
import math
from typing import Optional
import pygame
import random
from pygame.event import Event
from pygame.surface import Surface
from bullet import Bullet
from MovingPoint import MovingPoint, ScreenSize
import userEvents

class Asteroid:
    __StartSize = .005
    __StartSpeed = .0002
    __BreakSpeed = .0001

    def __init__(self, window: Surface, startSize: int, point: MovingPoint):
        self.__size = startSize
        self.__position = point
        self.__window = window

    def __draw(self) -> None:
        radius = self.__position.scale(self.__size * Asteroid.__StartSize)
        pygame.draw.circle(self.__window, (128,128,128), self.__position.getPosition(), radius, 2)
    
    def update(self, events: list[Event]) -> None:
        self.__position.coast()
        self.__draw()

    def checkForHits(self, bullet: Bullet) -> Optional[list[Asteroid]]:
        radius = self.__position.scale(self.__size * Asteroid.__StartSize)
        d = math.dist(self.__position.getPosition(), bullet.position)
        if d < radius:
            if self.__size == 1:
                return []
            else:
                direction = random.random()*180
                speed = self.__position.scale(Asteroid.__BreakSpeed)
                m1 = self.__position.launch(speed, direction)
                m2 = self.__position.launch(speed, direction+180)
                newSize = self.__size // 2
                return [Asteroid(self.__window, newSize, m1), Asteroid(self.__window, newSize, m2)]
        else:
            return None

    def handleResize(self, size: ScreenSize) -> None:
        self.__position.handleResize(size)

    @staticmethod
    def CreateStartAsteroid(window: Surface) -> Asteroid:
        (cx,cy) = window.get_size()
        startSize = 8
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
