from __future__ import annotations
import random
import time
from pygame.event import Event
from MovingPoint import MovingPoint, ScreenSize
from typing import Literal, Optional
import pygame
from pygame.surface import Surface
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


class Debris(GameObject):
    def __init__(self, window: Surface, position: MovingPoint):
        super().__init__()
        self._position = position
        self._window = window
        self._gameOverTime = time.time() + 1 + random.random()*1.5

    def checkForCollision(self, other: GameObject) -> bool:
        return False

    def handleCollision(self, impactedWith: GameObject) -> None:
        return
    
    def update(self, events: list[Event]) -> None:
        self._position.coast()
        super().update(events)
        if time.time() > self._gameOverTime:
            AsteroidsEvent.PostRemoveEvent(self)
    
    def _draw(self) -> None:
        (cx,cy) = self._position.getPosition()
        pygame.draw.circle(self._window, (255,255,255), (cx,cy), 2)

class DotDebris(Debris):
    def __init__(self, window: Surface, position: MovingPoint):
        super().__init__(window, position)
    
    def _draw(self) -> None:
        (cx,cy) = self._position.getPosition()
        pygame.draw.circle(self._window, (255,255,255), (cx,cy), 2)

class LineDebris(Debris):
    def __init__(self, window: Surface, position: MovingPoint, baseLength: float):
        super().__init__(window, position)
        self._angle = random.random()*math.pi
        self._rotationRate = random.random()*.05
        self._lineLength = baseLength*(.5 + random.random())
    
    def _draw(self) -> None:
        (cx,cy) = self._position.getPosition()
        self._angle += self._rotationRate
        pygame.draw.line(self._window, (255,255,255),
            (cx-math.cos(self._angle)*self._lineLength,cy-math.sin(self._angle)*self._lineLength),
            (cx+math.cos(self._angle)*self._lineLength,cy+math.sin(self._angle)*self._lineLength), 3)



Factions = Literal['player', 'asteroids', 'aliens']

class MobileGameObject(GameObject):
    def __init__(self, window: Surface, faction: Factions, position: MovingPoint):
        super().__init__()
        self._position = position
        self.__faction = faction
        self._window = window
        self._debrisType : Literal['dots', 'lines', 'none'] = 'dots'
    
    @property
    def _radius(self) -> float:
        return 0
    
    def update(self, events: list[Event]) -> None:
        self._position.coast()
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self._position.handleResize(self._window.get_size())
        super().update(events)

    def checkForCollision(self, other: GameObject) -> bool:
        return isinstance(other, MobileGameObject) \
           and self.__faction != other.__faction \
           and math.dist(self._position.getPosition(), other._position.getPosition()) < other._radius + self._radius

    def handleCollision(self, impactedWith: GameObject) -> None:
        super().handleCollision(impactedWith)
        if self._debrisType != 'none':
            for _ in range(12 if self._debrisType == 'dots' else 6):
                trajectory = self._position.launch(0.2 + random.random()*.2, random.random()*360)
                d = DotDebris(self._window, trajectory) if self._debrisType == 'dots' else LineDebris(self._window, trajectory, self._position.scale(.003))
                AsteroidsEvent.PostAddEvent(d)

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