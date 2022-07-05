import math
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

    def __init__(self, window: Surface):
        (cx,cy) = window.get_size()
        self.__size = 8
        size = min(cx, cy) * Asteroid.__StartSize * self.__size

        startSide = random.choice(['left', 'right', 'top', 'bottom'])
        if startSide == 'left':
            x = -size
            y = random.randint(0, cy)
            if y < cy/2:
                direction = -random.random()*80
            else:
                direction = random.random()*80
        else:
            x = cx+size
            y = random.randint(0, cy)
            if y < cy/2:
                direction = 180+random.random()*80
            else:
                direction = 180-random.random()*80
        
        dx = Asteroid.__StartSpeed*cx*math.cos(math.radians(direction))
        dy = -Asteroid.__StartSpeed*cy*math.sin(math.radians(direction))
        self.__position = MovingPoint(x, y, dx, dy, (cx,cy))
        self.__window = window
        self.__direction = 0

    def __draw(self) -> None:
        radius = self.__position.scale(self.__size * Asteroid.__StartSize)
        pygame.draw.circle(self.__window, (128,128,128), self.__position.getPosition(), radius, 2)
    
    def update(self, events: list[Event]) -> None:
        self.__position.coast()
        self.__draw()

    def handleResize(self, size: ScreenSize) -> None:
        self.__position.handleResize(size)