
# To install requirements:
#  py -m pip uninstall pygame
#  py -m pip install pygame_widgets

#TODO:
#   Make small UFO's be sharpshooters
#   Make sounds
#   Give bonus for wave clear
#   Make the asteroids look better
#   High Score
#   Make hyperspace button
#   Make there be jet exhaust that you can actually see
#
# TickyTack:
#   Shouldn't score for asteroids blown up by aliens?

import random
import pygame
from pygame.event import Event
from Asteroid import Asteroid
from GameObject import GameObject, AsteroidsEvent
from Score import Score
from Tweakables import Balance
from aliens import Alien, BigAlien, SmallAlien
from ship import Ship
from pygame.font import SysFont
import time

class AsteroidsGame:
    def __init__(self):
        self.__window = pygame.display.set_mode((0, 0), pygame.RESIZABLE, display=0)
        self.__objects: list[GameObject] = []
        self.__closing = False
        self.__gameOverFont = SysFont('arial', 192)
        self.__livesCount = 0
        self.__pendingNewShip = False
        self.__crashTime: float = 0

    def __startPressed(self) -> None:
        if self.__livesCount > 0:
            return
        self.__livesCount = 3
        self.__objects.clear()
        self.__objects.append(Score(self.__window))
        self.__objects.append(Ship(self.__window))
        for _ in range(Balance.ASTEROIDS_IN_STARTING_WAVE):
            a = Asteroid.CreateStartAsteroid(self.__window)
            self.__objects.append(a)
        return
    
    def __shipBlownUp(self) -> None:
        self.__livesCount -= 1
        if self.__livesCount > 0:
            self.__pendingNewShip = True
            self.__crashTime = time.time()

    def __checkForShipSpawn(self) -> None:
        if self.__pendingNewShip and time.time() > self.__crashTime + 2:
            # TODO: Make sure the center is clear
            self.__objects.append(Ship(self.__window))
            self.__pendingNewShip = False

    def __update(self, events: list[Event]) -> None:
        self.__checkForShipSpawn()
        self.__spawnAliens()
        for event in events:
            asteroidsEvent = AsteroidsEvent.TryGetFromEvent(event)
            if event.type == pygame.QUIT:
                self.__closing = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.__startPressed()
            elif asteroidsEvent is not None:
                if asteroidsEvent.type == 'add':
                    self.__objects.append(asteroidsEvent.object)
                elif asteroidsEvent.type == 'remove':
                    self.__objects.remove(asteroidsEvent.object)    #   Bug here (list.remove(x): x not in list)
                    if isinstance(asteroidsEvent.object, Ship):
                        self.__shipBlownUp()
        for o in self.__objects:
            o.update(events)
        self.__draw()

    def __draw(self) -> None:
        if self.__livesCount == 0:
            gameOverImage = self.__gameOverFont.render(f"Game Over", True, (255,0,0))
            imageRect = gameOverImage.get_rect()
            (cx,cy) = self.__window.get_size()
            self.__window.blit(gameOverImage, (cx/2 - imageRect.width/2, cy/2 - imageRect.height/2))
        else:
            for i in range(self.__livesCount-1):
                (cx,cy) = self.__window.get_size()
                w = cx * .005
                h = cy * .02
                sx = cx * .001 # Spacing between ships in the x direction
                px = sx  # Padding in the x direction
                py = cy * .002 # Padding in the y direction
                pygame.draw.polygon(self.__window, (255,255,255), [
                    (px+i*(w+sx)+w/2, py),
                    (px+i*(w+sx), py+h),
                    (px+i*(w+sx)+w, py+h)], width=2)

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
    
    def __checkIfWaveCleared(self) -> None:
        if not any([x for x in self.__objects if isinstance(x, Asteroid)]):
            for _ in range(8):
                a = Asteroid.CreateStartAsteroid(self.__window)
                self.__objects.append(a)
    
    def __spawnAliens(self) -> None:
        if not any([x for x in self.__objects if isinstance(x, Alien)]):
            if random.random() <= .005:
                a = SmallAlien(self.__window) if random.random() < .3 else BigAlien(self.__window)
                self.__objects.append(a)

    def main(self) -> None:
        pygame.display.set_caption("Asteroids")
        # pygame.display.set_icon(pygame.image.load("icon.png"))

        while not self.__closing:
            self.__window.fill((0,0,0))
            self.__update(pygame.event.get())
            pygame.display.update()
            self.__checkCollisions()
            if self.__livesCount > 0:
                self.__checkIfWaveCleared()
            time.sleep(.01)


pygame.init()
pygame.font.init()
AsteroidsGame().main()
