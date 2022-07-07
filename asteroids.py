
# To install requirements:
#  py -m pip uninstall pygame
#  py -m pip install pygame_widgets

# TODO:
#   Make the asteroids look better
#   Make there be jet exhaust
#   Make the ship able to die
#   Recognize no more asteroids and start a new wave
#   Keep score
#   High Score
#   Make sounds
#   Make hyperspace button
#   Make Big UFO's appear
#   Make Small UFO's appear
#   Make a game-over button
#   Make high scores

from typing import Optional
import pygame
from pygame.event import Event
from Asteroid import Asteroid
from bullet import Bullet
from ship import Ship
import time
import userEvents

class AsteroidsGame:

    def __init__(self):
        self.__window = pygame.display.set_mode((0, 0), pygame.RESIZABLE, display=0)
        self.score: int = 0
        self.ship: Ship = Ship(self.__window)
        self.asteroids: list[Asteroid] = []
        for _ in range(8):
            a = Asteroid.CreateStartAsteroid(self.__window)
            self.asteroids.append(a)
        self.bullets : list[Bullet] = []

    def __handleResize(self) -> None:
        sz = self.__window.get_size()
        self.ship.handleResize(sz)
        for b in self.bullets:
            b.handleResize(sz)

    def main(self) -> None:
        pygame.display.set_caption("Asteroids")
        # pygame.display.set_icon(pygame.image.load("icon.png"))
        pygame.display.update()

        closing = False
        while not closing:
            self.__window.fill((0,0,0))
            unhandledEvents: list[Event] = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closing = True
                elif event.type == userEvents.BULLET:
                    if event.action == 'add':
                        self.bullets.append(event.bullet)
                    else:
                        assert event.action == 'delete'
                        self.bullets.remove(event.bullet)
                elif event.type == pygame.VIDEORESIZE:
                    self.__handleResize()
                # TODO: More if statements.
                else:
                    unhandledEvents.append(event)
            self.ship.update(unhandledEvents)
            for b in self.bullets:
                b.update(unhandledEvents)
            for b in self.asteroids:
                b.update(unhandledEvents)
            pygame.display.update()

            newAsteroids: list[Asteroid] = []
            deadAsteroids: list[Asteroid] = []
            for a in self.asteroids:
                deadBullet: Optional[Bullet] = None
                for b in self.bullets:
                    splits = a.checkForHits(b)
                    if splits is not None:
                        newAsteroids += splits
                        deadAsteroids.append(a)
                        deadBullet = b
                if deadBullet:
                    self.bullets.remove(deadBullet)
            for a in deadAsteroids:
                self.asteroids.remove(a)
            self.asteroids += newAsteroids

            time.sleep(.01)

pygame.init()
pygame.font.init()
AsteroidsGame().main()
