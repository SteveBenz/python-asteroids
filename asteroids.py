

# To install requirements:
#  py -m pip uninstall pygame
#  py -m pip install pygame_widgets

import pygame
from pygame.event import Event
from bullet import Bullet
from ship import Ship
import time

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
        return

pygame.init()
pygame.font.init()
AsteroidsGame().main()
