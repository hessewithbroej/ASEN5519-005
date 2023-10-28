import pygame
import sys

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

pygame.init()
disp_width = 700
disp_height = 700
win = pygame.display.set_mode((disp_width, disp_height))
pygame.display.set_caption("N-Back Testing")

prompt_font = pygame.font.Font('freesansbold.ttf',44)

while True:

    win.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # a key was pressed
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_j:
                text = prompt_font.render("  j  ", True, white, blue)
                textRect = text.get_rect()
                textRect.center = (disp_width/2, disp_height/2)
                win.blit(text,textRect)

        pygame.display.update()
