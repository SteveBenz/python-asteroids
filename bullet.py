from MovingPoint import MovingPoint
from GameObject import MobileGameObject, AsteroidsEvent
import pygame
from pygame.event import Event
from pygame.surface import Surface
from typing import Literal
from Tweakables import Balance, Colors

class Bullet(MobileGameObject):
    def __init__(self, window: Surface, faction: Literal['player','aliens'], position: MovingPoint):
        super().__init__(window, faction, position)
        self.__age = 0
        self._debrisType = 'none'
        self.__color = Colors.PLAYER_BULLET if faction == 'player' else Colors.ALIEN_BULLET

    @property
    def _radius(self) -> float:
        return 3

    def update(self, events: list[Event]) -> None:
        super().update(events)
        self.__age += 1
        if self.__age > Balance.BULLET_LIFETIME:
            AsteroidsEvent.PostRemoveEvent(self)

    def _draw(self) -> None:
        pygame.draw.circle(self._window, self.__color, self._position.getPosition(), self._radius)

