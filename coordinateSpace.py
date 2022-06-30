from pygame.rect import Rect
from pygame.surface import Surface
from typing import Tuple

GamePoint = Tuple[float, float]

class Velocity:
    def __init__(self, speed: float, direction: float):
        self.speed = speed
        self.direction = direction
    
    def turn(self, amount: float) -> None:
        self.direction += amount

    def accelerate(self, amount: float) -> None:
        self.speed += amount

def mapPoint(point: GamePoint, window: Surface) -> Tuple[int,int]:
    (x,y) = point
    (sz_x, sz_y) = window.get_size()
    return (int(sz_x*x),int(y*sz_y))

# def mapRect(r: Rect) -> Rect

def move(point: GamePoint, velocity: Velocity) -> GamePoint:
    return (0,0)

