from __future__ import annotations
from pygame.event import Event
from MovingPoint import MovingPoint, ScreenSize
from typing import Literal, Optional
import pygame
import math

class GameObject:
    def update(self, events: list[Event]) -> None:
        self._draw()
    
    def _draw(self) -> None:
        return

    def checkForCollision(self, other: GameObject) -> bool:
        return False

    def handleCollision(self, impactedWith: GameObject) -> None:
        AsteroidsEvent.PostRemoveEvent(self)
        # pygame.event.post(Event(pygame.USEREVENT, **{'action': 'remove', 'item': self}))

    def handleResize(self, size: ScreenSize) -> None:
        return

Factions = Literal['player', 'asteroids', 'aliens']

class MobileGameObject(GameObject):
    def __init__(self, faction: Factions, position: MovingPoint):
        super().__init__()
        self._position = position
        self.__faction = faction
    
    @property
    def _radius(self) -> float:
        return 0
    
    def update(self, events: list[Event]) -> None:
        self._position.coast()
        super().update(events)

    def checkForCollision(self, other: GameObject) -> bool:
        return isinstance(other, MobileGameObject) \
           and self.__faction != other.__faction \
           and math.dist(self._position.getPosition(), other._position.getPosition()) < other._radius + self._radius

    def handleResize(self, size: ScreenSize) -> None:
        self._position.handleResize(size)


EventTypes = Literal['add', 'remove']

class AsteroidsEvent:
    def __init__(self, t: EventTypes, o: 'GameObject'):
        self.__type: EventTypes = t
        self.__object = o
    
    @property
    def type(self) -> EventTypes:
        return self.__type

    @property
    def object(self) -> GameObject:
        return self.__object

    def __post(self) -> None:
        pygame.event.post(Event(pygame.USEREVENT, **{'eventData': self}))

    @staticmethod
    def PostAddEvent(o: GameObject) -> None:
        AsteroidsEvent('add', o).__post()

    @staticmethod
    def PostRemoveEvent(o: GameObject) -> None:
        AsteroidsEvent('remove', o).__post()

    @staticmethod
    def TryGetFromEvent(e: Event) -> Optional[AsteroidsEvent]:
        if e.type == pygame.USEREVENT:
            assert isinstance(e.eventData, AsteroidsEvent)
            return e.eventData
        else:
            return None