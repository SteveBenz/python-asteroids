from __future__ import annotations
from pygame.rect import Rect
from pygame.surface import Surface
from typing import Tuple
import math

GamePoint = Tuple[float, float]

class Velocity:
    def __init__(self):
        self.__dx: float = 0
        self.__dy: float = 0

    def accelerate(self, amount: float, direction: float) -> Velocity:
        directionInRadians = direction*math.pi / 180
        v = Velocity()
        v.__dx = self.__dx + amount * math.cos(directionInRadians)
        v.__dy = self.__dy - amount * math.sin(directionInRadians)
        return v

    def move(self, point: GamePoint) -> GamePoint:
        (x,y) = point
        x = (x + self.__dx) % 1
        y = (y + self.__dy) % 1
        return (x,y)

def mapPoint(point: GamePoint, window: Surface) -> Tuple[int,int]:
    (x,y) = point
    (sz_x, sz_y) = window.get_size()
    return (int(sz_x*x),int(y*sz_y))

# def mapRect(r: Rect) -> Rect

