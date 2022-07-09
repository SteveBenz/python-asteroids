
# To install requirements:
#  py -m pip uninstall pygame
#  py -m pip install pygame_widgets

# TODO:
#   Crash animation
#   Sparkles animation when asteroid gets shot
#   Send in a new batch of asteroids when wave is cleared
#   Make sounds
#   Make the asteroids look better
#   High Score
#   Make hyperspace button
#   Make Big UFO's appear
#   Make Small UFO's appear
#
# TickyTack:
#   Make there be jet exhaust
#   Score more for different asteroids
#   Shouldn't score for asteroids blown up by aliens?
#   Asteroids get blown into 8 parts, not 16
#   Ship should have friction

import pygame
from pygame.event import Event
from Asteroid import Asteroid
from GameObject import GameObject, AsteroidsEvent
from Score import Score
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
        for _ in range(8):
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
        for event in events:
            asteroidsEvent = AsteroidsEvent.TryGetFromEvent(event)
            if event.type == pygame.QUIT:
                self.__closing = True
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                self.__startPressed()
            elif asteroidsEvent is not None:
                if asteroidsEvent.type == 'add':
                    self.__objects.append(asteroidsEvent.object)
                elif asteroidsEvent.type == 'remove':
                    self.__objects.remove(asteroidsEvent.object)
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
