from GameObject import AsteroidsEvent, MobileGameObject, MovingPoint, GameObject
from pygame.surface import Surface
import time
import pygame
from pygame.event import Event
import random

class Debris(MobileGameObject):
    def __init__(self, window: Surface, position: MovingPoint):
        super().__init__(window, 'debris', position)
        self.__gameOverTime = time.time() + 1 + random.random()*1.5

    def checkForCollision(self, other: GameObject) -> bool:
        return False

    def handleCollision(self, impactedWith: GameObject) -> None:
        return
    
    def update(self, events: list[Event]) -> None:
        self._position.coast()
        super().update(events)
        if time.time() > self.__gameOverTime:
            AsteroidsEvent.PostRemoveEvent(self)
    
    def _draw(self) -> None:
        (cx,cy) = self._position.getPosition()
        pygame.draw.circle(self._window, (255,255,255), (cx,cy), 2)
