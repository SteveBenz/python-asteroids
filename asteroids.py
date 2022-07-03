
# To install requirements:
#  py -m pip uninstall pygame
#  py -m pip install pygame_widgets

# TODO:
#   Make the ship shoot
#   Fix the coordinate space so it's not width=height
#   Make asteroids float around
#   Make asteroids able to get shot
#   Make the ship able to die
#   Keep score
#   High Score
#   Make the asteroids look better
#   Make there be jet exhaust


import pygame
from pygame.event import Event
from bullet import Bullet
from ship import Ship
import time
import userEvents

class AsteroidsGame:

    def __init__(self):
        self.__window = pygame.display.set_mode((0, 0), pygame.RESIZABLE, display=0)
        self.score: int = 0
        self.ship: Ship = Ship(self.__window)
        self.asteroids = []
        self.bullets : list[Bullet] = []
        return

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
                # elif event.type == pygame.VIDEORESIZE:
                #     self.__onResize()
                # TODO: More if statements.
                else:
                    unhandledEvents.append(event)
            self.ship.update(unhandledEvents)
            for b in self.bullets:
                b.update(unhandledEvents)
            pygame.display.update()
            time.sleep(.01)

pygame.init()
pygame.font.init()
AsteroidsGame().main()
