import pygame
from pygame.event import Event
from coordinateSpace import Velocity
from coordinateSpace import GamePoint

class Ship:
    __AccelerationRate = .01
    __TurnRate = .01

    def __init__(self):
        self.velocity: Velocity = Velocity(speed=0, direction=0)
        self.position: GamePoint = (0,0)
        return

    def update(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.velocity.accelerate(Ship.__AccelerationRate)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.velocity.turn(0-Ship.__TurnRate)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.velocity.turn(Ship.__TurnRate)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                
        
        return