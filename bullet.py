from MovingPoint import MovingPoint
from GameObject import MobileGameObject, AsteroidsEvent, Factions
import pygame
from pygame.event import Event
from pygame.surface import Surface
import time

class Bullet(MobileGameObject):
    def __init__(self, window: Surface, faction: Factions, position: MovingPoint):
        super().__init__(window, faction, position)
        self.__endTime = time.time() + 3 #  Our bullets last 3 seconds

    @property
    def _radius(self) -> float:
        return 3

    def update(self, events: list[Event]) -> None:
        super().update(events)
        if time.time() > self.__endTime:
            AsteroidsEvent.PostRemoveEvent(self)

    def _draw(self) -> None:
        pygame.draw.circle(self._window, (128,255,128), self._position.getPosition(), self._radius)

