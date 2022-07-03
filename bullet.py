from coordinateSpace import GamePoint, mapPoint
from coordinateSpace import Velocity
import pygame
from pygame.event import Event
from pygame.surface import Surface
import time
import userEvents

class Bullet:
    def __init__(self, window: Surface, point: GamePoint, velocity: Velocity):
        self.__window = window
        self.__position = point
        self.__velocity = velocity
        self.__endTime = time.time() + 3 #  Our bullets last 3 seconds

    def update(self, events: list[Event]) -> None:
        self.__position = self.__velocity.move(self.__position)
        self.__draw()
        if time.time() > self.__endTime:
            pygame.event.post(Event(userEvents.BULLET, **{'bullet': self, 'action': 'delete'}))
    
    def __draw(self) -> None:
        (cx, cy) = mapPoint(self.__position, self.__window)
        pygame.draw.circle(self.__window, (128,255,128), (cx,cy), 3)

