from __future__ import annotations
import math
import pygame
import random
from pygame.event import Event
from pygame.surface import Surface
from MovingPoint import MovingPoint
from GameObject import GameObject, MobileGameObject, AsteroidsEvent
from Tweakables import Balance, Scoring, Sizes

class Asteroid(MobileGameObject):
    def __init__(self, window: Surface, position: MovingPoint):
        super().__init__(window, 'asteroids', position)

    def _draw(self) -> None:
        pygame.draw.circle(self._window, (128,128,128), self._position.getPosition(), self._radius, 2)

    def update(self, events: list[Event]) -> None:
        super().update(events)

    def _makeChild(self, movingPoint: MovingPoint) -> None:
        pass

    def handleCollision(self, impactedWith: GameObject) -> None:
        super().handleCollision(impactedWith)
        direction = random.random()*180
        speed = self._position.scale(Balance.ASTEROID_BREAK_SPEED)
        self._makeChild(self._position.launch(speed, direction))
        self._makeChild(self._position.launch(speed, direction+180))

    @staticmethod
    def CreateStartAsteroid(window: Surface) -> Asteroid:
        (cx,cy) = window.get_size()
        size = min(cx, cy) * Sizes.ASTEROID_BIG

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
        
        dx = Balance.ASTEROID_SPEED*cx*math.cos(math.radians(direction))
        dy = -Balance.ASTEROID_SPEED*cy*math.sin(math.radians(direction))
        return BigAsteroid(window, MovingPoint(x, y, dx, dy, (cx,cy)))

class SmallAsteroid(Asteroid):
    @property
    def _radius(self) -> float:
        return self._position.scale(Sizes.ASTEROID_SMALL)

    def getScore(self) -> int:
         return Scoring.ASTEROID_SMALL

    def _makeChild(self, movingPoint: MovingPoint) -> None:
        return

class MediumAsteroid(Asteroid):
    @property
    def _radius(self) -> float:
        return self._position.scale(Sizes.ASTEROID_MEDIUM)

    def getScore(self) -> int:
         return Scoring.ASTEROID_MEDIUM

    def _makeChild(self, movingPoint: MovingPoint) -> None:
        AsteroidsEvent.PostAddEvent(SmallAsteroid(self._window, movingPoint))

class BigAsteroid(Asteroid):
    @property
    def _radius(self) -> float:
        return self._position.scale(Sizes.ASTEROID_BIG)

    def getScore(self) -> int:
         return Scoring.ASTEROID_BIG

    def _makeChild(self, movingPoint: MovingPoint) -> None:
        AsteroidsEvent.PostAddEvent(MediumAsteroid(self._window, movingPoint))
