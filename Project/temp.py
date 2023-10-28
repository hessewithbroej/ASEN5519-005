import itertools
import pygame
import os

class Scene:
    def on_draw(self, surface): pass
    def on_update(self, delta): pass
    def on_event(self, event): pass

class Manager:
    @classmethod
    def create(cls, title, width, height, center=False):
        if center:
            os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Basic pygame setup
        pygame.display.set_caption(title)
        cls.surface = pygame.display.set_mode((width, height))
        cls.rect = cls.surface.get_rect()
        cls.clock = pygame.time.Clock()
        cls.running = False
        cls.delta = 0
        cls.fps = 60

        cls.scene = Scene()

    @classmethod
    def mainloop(cls):
        cls.running = True
        while cls.running:
            for event in pygame.event.get():
                cls.scene.on_event(event)

            cls.scene.on_update(cls.delta)
            cls.scene.on_draw(cls.surface)

            pygame.display.flip()
            cls.delta = cls.clock.tick(cls.fps)

class TextTimed:
    def __init__(self, font, text, foreground, position, timed=3000, anchor="topleft"):
        self.image = font.render(text, 1, foreground)
        self.rect = self.image.get_rect()
        setattr(self.rect, anchor, position)
        self.timed = timed

    def draw(self, surface):
        if self.timed > 0:
            surface.blit(self.image, self.rect)

    def update(self, delta):
        self.timed -= delta

class Example(Scene):
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.timed_text = []
        self.count = itertools.count(1, 1)

    def position_text(self):
        y = itertools.count(Manager.rect.bottom - 50, -30)
        for text in self.timed_text[::-1]:
            text.rect.y = next(y)

    def on_draw(self, surface):
        surface.fill(pygame.Color("black"))
        for text in self.timed_text:
            text.draw(surface)

    def on_update(self, delta):
        timed_text = []
        for text in self.timed_text:
            text.update(delta)
            if text.timed > 0:
                timed_text.append(text)

        self.timed_text = timed_text
        self.position_text()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            Manager.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                text = "Timed Text {}".format(next(self.count))
                color = pygame.Color("dodgerblue")
                timed = TextTimed(self.font, text, color, (20, 0))
                self.timed_text.append(timed)
                self.position_text()

def main():
    pygame.init()
    Manager.create("Example Timed Text", 800, 600, True)
    Manager.scene = Example()
    Manager.mainloop()

main()