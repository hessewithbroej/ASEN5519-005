import pygame
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt


class Prompt:
    pygame.font.init()
    DEFAULT_FONT = pygame.font.Font('freesansbold.ttf',46)

    def __init__(self, win, text, visible_timer, respondable_timer):

        disp_width,disp_height  = win.get_size()

        text = "  " + text + "  "

        self.fontObj = self.DEFAULT_FONT.render(text, True, (255,255,255), (0,0,128))
        self.rect = self.fontObj.get_rect()
        self.rect.center = (disp_width/2, disp_height/2)
        self.visible_timer = visible_timer
        self.respondable_timer = respondable_timer

    def draw(self, win):
        #when attempting to draw prompt text,if there is no time remaining, erase prompt
        if self.visible_timer > 0:
            win.blit(self.fontObj, self.rect)
        else:
            win.fill((255, 255, 255))

    def update(self, dt):
        self.visible_timer -= dt
        self.respondable_timer -= dt