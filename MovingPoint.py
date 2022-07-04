from __future__ import annotations
from typing import Tuple
import math

ScreenSize = Tuple[int, int]

class MovingPoint:
    def __init__(self, x: float, y: float, dx: float, dy: float, screenSize: ScreenSize):
        assert x >= 0 and x < screenSize[0]
        assert y >= 0 and y < screenSize[1]
        self.__size = screenSize
        self.__x = x
        self.__y = y
        self.__dx = dx
        self.__dy = dy
    
    def handleResize(self, newSize: Tuple[int,int]) -> None:
        self.__x *= newSize[0] / self.__size[0]
        self.__y *= newSize[1] / self.__size[1]
        self.__dx *= newSize[0] / self.__size[0]
        self.__dy *= newSize[1] / self.__size[1]
        self.__size = newSize

    def getPosition(self) -> Tuple[float,float]:
        return (self.__x,self.__y)
    
    def accelerate(self, amount: float, direction: float) -> None:
        directionInRadians = direction*math.pi / 180
        self.__dx = self.__dx + amount * math.cos(directionInRadians)
        self.__dy = self.__dy - amount * math.sin(directionInRadians)
    
    def coast(self) -> None:
        self.__x = (self.__x + self.__dx) % self.__size[0]
        self.__y = (self.__y + self.__dy) % self.__size[1]

    def launch(self, amount: float, direction: float) -> MovingPoint:
        directionInRadians = direction*math.pi / 180
        dx = self.__dx + amount * math.cos(directionInRadians)
        dy = self.__dy - amount * math.sin(directionInRadians)
        return MovingPoint(self.__x, self.__y, dx, dy, self.__size)
    
    def scale(self, fractionalAmount: float) -> float:
        return min(self.__size[0], self.__size[1])*fractionalAmount
