

# To install requirements:
#  py -m pip uninstall pygame
#  py -m pip install pygame_widgets

import pygame
from pygame.event import Event
from bullet import Bullet
from ship import Ship

class AsteroidsGame:

    def __init__(self):
        self.score: int = 0
        self.ship: Ship = Ship()
        self.asteroids = []
        self.bullets : list[Bullet] = []
        return

    def main(self) -> None:
        pygame.display.set_caption("Asteroids")
        # pygame.display.set_icon(pygame.image.load("icon.png"))
        pygame.display.update()

        closing = False
        while not closing:
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
        return

pygame.init()
pygame.font.init()
AsteroidsGame().main()
