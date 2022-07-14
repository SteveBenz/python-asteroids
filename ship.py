import pygame
from pygame.event import Event
from pygame.surface import Surface
from bullet import Bullet
from MovingPoint import MovingPoint
from GameObject import MobileGameObject, AsteroidsEvent

class Ship(MobileGameObject):
    __AccelerationRate = 0.00002
    __TurnRate = 2
    __BulletSpeed = 0.005
    __ShipSize = 0.02

    def __init__(self, window: Surface):
        (cx,cy) = window.get_size()
        super().__init__(window, 'player', MovingPoint(cx/2, cy/2, 0, 0, (cx,cy)))
        self.__direction = 0
        self.__isTurningCcw = False
        self.__isTurningCw = False
        self.__isAccelerating = False
        self._debrisType = 'lines'

    @property
    def _radius(self) -> float:
        # Note that radius is the one used for collisions - and we make the contact area just a bit smaller
        # to not enrage players because the radius doesn't conform to the triangle of the ship
        return self._position.scale(Ship.__ShipSize*.6)

    def _draw(self) -> None:
        sizeX = sizeY = self._position.scale(Ship.__ShipSize)
        shipImage = pygame.Surface((sizeX,sizeY), pygame.SRCALPHA)
        if self.__isAccelerating == False:
            pygame.draw.polygon(shipImage, (255,255,255),
                        [(sizeX, sizeY/2),
                        (0, sizeY/6),
                        (sizeX/10, sizeY/2),
                        (0, 5*sizeY/6)], width=2)
        else:
            pygame.draw.polygon(shipImage, (255,255,255),
                        [(sizeX, sizeY/2),
                        (0, sizeY/6),
                        (sizeX/10, sizeY/2),
                        (0, 5*sizeY/6),
                        (0, sizeY/6),
                        (0, 5*sizeY/6)], width=2)
        shipImage = pygame.transform.rotate(shipImage, self.__direction)
        (sizeX, sizeY) = shipImage.get_size()
        (cx,cy) = self._position.getPosition()
        self._window.blit(shipImage, (cx - sizeX/2, cy - sizeY/2))
    
    def __shoot(self) -> None:
        b = Bullet(self._window, 'player', self._position.launch(self._position.scale(Ship.__BulletSpeed), self.__direction))
        AsteroidsEvent.PostAddEvent(b)

    def update(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.__isAccelerating = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_w:
                self.__isAccelerating = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.__isTurningCcw = True
                self.__isTurningCw = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_a:
                self.__isTurningCcw = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.__isTurningCw = True
                self.__isTurningCcw = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                self.__isTurningCw = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__shoot()

        if self.__isAccelerating:
            self._position.accelerate(self._position.scale(Ship.__AccelerationRate), self.__direction)
        if self.__isTurningCcw:
            self.__direction += Ship.__TurnRate
        if self.__isTurningCw:
            self.__direction -= Ship.__TurnRate
        
        super().update(events)
