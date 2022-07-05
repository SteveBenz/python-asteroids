from typing import Tuple
from MovingPoint import MovingPoint, ScreenSize
import pygame
from pygame.event import Event
from pygame.surface import Surface
import time
import userEvents

class Bullet:
    def __init__(self, window: Surface, point: MovingPoint):
        self.__window = window
        self.__position = point
        self.__endTime = time.time() + 3 #  Our bullets last 3 seconds

    def update(self, events: list[Event]) -> None:
        self.__position.coast()
        self.__draw()
        if time.time() > self.__endTime:
            pygame.event.post(Event(userEvents.BULLET, **{'bullet': self, 'action': 'delete'}))

    def handleResize(self, size: ScreenSize) -> None:
        self.__position.handleResize(size)
    
    def __draw(self) -> None:
        pygame.draw.circle(self.__window, (128,255,128), self.__position.getPosition(), 3)
    
    @property
    def position(self) -> Tuple[float,float]:
        return self.__position.getPosition()

