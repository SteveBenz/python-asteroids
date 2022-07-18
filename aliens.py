import random
import pygame
from pygame.event import Event
from pygame.surface import Surface
from bullet import Bullet
from MovingPoint import MovingPoint
from GameObject import MobileGameObject, AsteroidsEvent

class Alien(MobileGameObject):
    __BulletSpeed = 0.005
    __ShipSize = 0.02

    def __init__(self, window: Surface):
        (cx,cy) = window.get_size()
        super().__init__(window, 'aliens', MovingPoint(cx/4, cy/4, 0, 0, (cx,cy)))
        self._debrisType = 'lines'

    @property
    def _radius(self) -> float:
        # Note that radius is the one used for collisions - and we make the contact area just a bit smaller
        # to not enrage players because the radius doesn't conform to the triangle of the ship
        return self._position.scale(Alien.__ShipSize*.6)

    def _draw(self) -> None:
        sizeX = sizeY = self._position.scale(Alien.__ShipSize)
        shipImage = pygame.Surface((sizeX,sizeY), pygame.SRCALPHA)
        pygame.draw.polygon(shipImage, (255,165,0),
                    [(sizeX, sizeY/3),
                    (0, sizeY/3),
                    (sizeX, sizeY/3),
                    (sizeX/3*2, 0),
                    (sizeX/3, 0),
                    (0, sizeY/3),
                    (sizeX/3, sizeY/3*2),
                    (sizeX/3*2, sizeY/3*2)], width=2)
        (sizeX, sizeY) = shipImage.get_size()
        (cx,cy) = self._position.getPosition()
        self._window.blit(shipImage, (cx - sizeX/2, cy - sizeY/2))
    
    def __shoot(self) -> None:
        d = random.random()*360
        b = Bullet(self._window, 'aliens', self._position.launch(self._position.scale(Alien.__BulletSpeed), d))
        AsteroidsEvent.PostAddEvent(b)

    def update(self, events: list[Event]) -> None:
        self._position.coast()
        if random.random() <= .01:
            self.__shoot()
        super().update(events)
