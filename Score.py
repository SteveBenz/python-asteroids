from GameObject import GameObject, AsteroidsEvent
from pygame.event import Event
from pygame.surface import Surface
from pygame.font import SysFont

class Score(GameObject):
    def __init__(self, window: Surface):
        super().__init__()
        self.__window = window
        self.__font = SysFont('arial', 48)
        self.__score = 0

    def update(self, events: list[Event]) -> None:
        for event in events:
            asteroidEvent = AsteroidsEvent.TryGetFromEvent(event)
            if asteroidEvent and asteroidEvent.type == 'remove':
                self.__score += asteroidEvent.object.getScore()
        self._draw()
    
    def _draw(self) -> None:
        scoreImage = self.__font.render(f"Score: {self.__score}", True, (192,192,255))
        imageRect = scoreImage.get_rect()
        (cx,_) = self.__window.get_size()
        self.__window.blit(scoreImage, (cx - 20 - imageRect.width, 5))
