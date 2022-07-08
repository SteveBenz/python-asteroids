
# To install requirements:
#  py -m pip uninstall pygame
#  py -m pip install pygame_widgets

# TODO:
#   Make the asteroids look better
#   Make there be jet exhaust
#   Make the ship able to die
#   Refactor to get rid of the special handleResize method
#   Recognize no more asteroids and start a new wave
#   Keep score
#   High Score
#   Make sounds
#   Make hyperspace button
#   Make Big UFO's appear
#   Make Small UFO's appear
#   Make a game-over button
#   Make high scores

import pygame
from pygame.event import Event
from Asteroid import Asteroid
from GameObject import GameObject, AsteroidsEvent
from Score import Score
from ship import Ship
import time

class AsteroidsGame:
    def __init__(self):
        self.__window = pygame.display.set_mode((0, 0), pygame.RESIZABLE, display=0)
        self.__objects: list[GameObject] = []
        self.__objects.append(Score(self.__window))
        self.__objects.append(Ship(self.__window))
        for _ in range(8):
            a = Asteroid.CreateStartAsteroid(self.__window)
            self.__objects.append(a)
        self.__closing = False

    def __handleResize(self) -> None:
        sz = self.__window.get_size()
        for b in self.__objects:
            b.handleResize(sz)

    def __update(self, events: list[Event]) -> None:
        for event in events:
            asteroidsEvent = AsteroidsEvent.TryGetFromEvent(event)
            if event.type == pygame.QUIT:
                self.__closing = True
            elif event.type == pygame.VIDEORESIZE:
                self.__handleResize()
            elif asteroidsEvent is not None:
                if asteroidsEvent.type == 'add':
                    self.__objects.append(asteroidsEvent.object)
                elif asteroidsEvent.type == 'remove':
                    self.__objects.remove(asteroidsEvent.object)
        for o in self.__objects:
            o.update(events)

    def __checkCollisions(self):
        uncollidedStuff = [o for o in self.__objects]
        i = 0
        while i < len(uncollidedStuff):
            oi = uncollidedStuff[i]
            j = i+1
            collisionHappened = False
            while not collisionHappened and j < len(uncollidedStuff):
                oj = uncollidedStuff[j]
                if oi.checkForCollision(oj):
                    oi.handleCollision(oj)
                    oj.handleCollision(oi)
                    uncollidedStuff.remove(oi)
                    uncollidedStuff.remove(oj)
                    collisionHappened = True
                else:
                    j += 1
            if not collisionHappened:
                i += 1

    def main(self) -> None:
        pygame.display.set_caption("Asteroids")
        # pygame.display.set_icon(pygame.image.load("icon.png"))

        while not self.__closing:
            self.__window.fill((0,0,0))
            self.__update(pygame.event.get())
            pygame.display.update()
            self.__checkCollisions()
            time.sleep(.01)


pygame.init()
pygame.font.init()
AsteroidsGame().main()
