import pygame
import sys
import Nback_game as nbg
from Prompt import *


class Manager:
    pygame.font.init()
    DEFAULT_FONT = pygame.font.Font('freesansbold.ttf',32)

    def __init__(self, game, disp_width = 700, disp_height = 700):
        self.game = game
        self.game_time = -1
        self.game_phase = "title"
        self.running = False
        self.disp_width = disp_width
        self.disp_height = disp_height
        self.clock=pygame.time.Clock()
        self.win = pygame.display.set_mode((disp_width, disp_height), flags=pygame.SCALED, vsync=1)
        pygame.display.set_caption("N-Back Testing")

    def display_text(self, string, location):
        txt_color = (0,0,0)
        bkg_color = (255,255,255)
        text = self.DEFAULT_FONT.render(string, True, txt_color, bkg_color)
        textRect = text.get_rect()
        textRect.center = (location[0], location[1])
        self.win.blit(text,textRect)

    def gameloop(self):

        self.running = True
        itrs = 0
        while self.running:
            itrs += 1 
            # print(f"Iterations: {itrs}")
            self.win.fill((255, 255, 255))

            if self.game_phase == "title":
                self.display_text("Title text. Press J to continue.", (self.disp_width/2,self.disp_height/2))
                
                for event in pygame.event.get():
                    #quit game when forced
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_j:
                            print("J WAS PRESSED")
                            seconds = 3
                            for i in range(seconds+1):
                                print(f"i: {i}")
                                self.win.fill((255, 255, 255))
                                text_string = f"Test Beginning in {seconds-i} seconds..."
                                self.display_text(text_string, (self.disp_width/2,self.disp_height/1.6))
                                pygame.display.update()
                                pygame.time.delay(1000)
                            self.game_phase = "playing"
                
            elif self.game_phase == "playing":

                #check to see if we have shown any prompts yet. First prompt shown.
                if self.game.get_current_prompt_ind() == 0:
                    prompt = Prompt(self.win, str(self.game.get_next_prompt()), self.game.prompt_time_visible, self.game.prompt_time_respond)
                    prompt.draw(self.win)
                    pygame.display.update()
                    self.clock.tick(30)
                    print(f"Displayed prompt {self.game.get_current_prompt_ind()} at time {self.clock.get_time()}")

                #we've shown at least one prompt
                else:

                    #check for keyboard input
                    for event in pygame.event.get():
                        #quit game when forced
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        #look for user response
                        if event.type == pygame.KEYDOWN:

                            #user suspects a match
                            if event.key == pygame.K_j:
                                print("J WAS PRESSED IN GAME - MATCH")

                            #user suspects no match
                            if event.key == pygame.K_f:
                                print("F WAS PRESSED IN GAME - NONMATCH")

                    #reduce visible time remaining on current prompt
                    #print(self.clock.tick_busy_loop())
                    prompt.update(self.clock.tick_busy_loop())
                    prompt.draw(self.win) #logic for checking whether still visible is inside prompt.draw
                    
                    #check to see if respond time has been passed
                    if prompt.respondable_timer < 0:
                        #get next prompt
                        prompt = Prompt(self.win, str(self.game.get_next_prompt()), self.game.prompt_time_visible, self.game.prompt_time_respond)
                        pygame.display.update()
                        self.clock.tick(30)
                        print(f"Displayed prompt {self.game.get_current_prompt_ind()} at time {self.clock.get_time()}")


                                    

            pygame.display.update()