from coordinateSpace import GamePoint
from coordinateSpace import Velocity
from coordinateSpace import move
from pygame.event import Event

class Bullet:
    def __init__(self, point: GamePoint, velocity: Velocity):
        self.__position = point
        self.__velocity = velocity
        self.__endTime = 3 # TODO: Now + something

    def update(self, events: list[Event]) -> None:
        self.__position = move(self.__position, self.__velocity)

        # TODO: Draw