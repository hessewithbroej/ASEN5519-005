import pygame
import sys
import Nback_game as nbg
from Prompt import *
from Trial import *


class Manager:
    pygame.font.init()
    DEFAULT_FONT = pygame.font.Font('freesansbold.ttf',32)

    def __init__(self, trial, disp_width = 700, disp_height = 700):
        self.trial = trial
        # self.game = self.trial.game
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
        
        flag_game_complete = False
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
                                self.win.fill((255, 255, 255))
                                text_string = f"Test Beginning in {seconds-i} seconds..."
                                self.display_text(text_string, (self.disp_width/2,self.disp_height/1.6))
                                pygame.display.update()
                                pygame.time.delay(1000)
                            self.game_phase = "info_enter"
            
            elif self.game_phase == "info_enter":
                self.display_text("If this is your first trial, press J.", (self.disp_width/2,self.disp_height/1.6))
                self.display_text("Otherwise, enter your 5-digit ID #.", (self.disp_width/2,self.disp_height/1.4))

                for event in pygame.event.get():
                    #quit game when forced
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_j:
                            print("J WAS PRESSED")
                            self.game_phase = "id_assignment"

            elif self.game_phase == "id_assignment":
                print("SKIPPING ID ASSIGNMENT...")
                self.game_phase = "playing"

            elif self.game_phase == "playing":
                
                #when user has answered all prompts in a given nback game/task, or its our first game
                if flag_game_complete or self.trial.current_task == 0:
                    if flag_game_complete:
                        self.win.fill((255, 255, 255))
                        self.display_text(f"Completed game number {self.trial.current_task} of {len(self.trial.task_sequence)}.", (self.disp_width/2,self.disp_height/1.6))
                        self.display_text(f"Overall Accuracy: {self.game.accuracy*100}%", (self.disp_width/2,self.disp_height/1.8))
                        pygame.display.update()
                        pygame.time.delay(5000)
                    
                    #only show countdown when tasks remaining
                    if self.trial.current_task < len(self.trial.task_sequence):
                        seconds = 5
                        for i in range(seconds+1):
                            self.win.fill((255, 255, 255))
                            text_string = f"Next game begins in {seconds-i} seconds..."
                            self.display_text(text_string, (self.disp_width/2,self.disp_height/1.6))
                            pygame.display.update()
                            pygame.time.delay(1000)

                    self.game = self.trial.serve_next_game()
                    #if we've completed all tasks
                    if self.game == None:
                        self.win.fill((255, 255, 255))
                        self.display_text("All games in trial have been completed.", (self.disp_width/2,self.disp_height/1.6))
                        self.display_text("Exiting", (self.disp_width/2,self.disp_height/1.8))
                        pygame.display.update()
                        pygame.time.delay(5000)
                        pygame.quit()
                        sys.exit()


                    flag_game_complete = False


                #completed the set of games/tasks. Move to finishing screen
                if self.game == None:
                    self.game_phase = "finished"
                    continue

                #check to see if we have shown any prompts yet. First prompt shown.
                if self.game.get_current_prompt_ind() == 0:
                    val = self.game.get_next_prompt()
                    prompt = Prompt(self.win, str(val), self.game.prompt_time_visible, self.game.prompt_time_respond)
                    prompt.draw(self.win)
                    flag_responded = False #only allow a single response per prompt
                    flag_correct = False
                    pygame.display.update()
                    self.clock.tick(30)
                    print(f"Displayed prompt {self.game.get_current_prompt_ind()}, value {val}, correct response {self.game.get_matches()[self.game.get_current_prompt_ind()-1]}")

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
                            if event.key == pygame.K_j and not flag_responded:
                                result = self.game.store_response(1)
                                flag_responded = True
                                flag_correct = result
                                print(f"{result}")

                            #user suspects no match
                            if event.key == pygame.K_f and not flag_responded:
                                result = self.game.store_response(0)
                                flag_responded = True
                                flag_correct = result
                                print(f"{result}")
                

                    #reduce visible time remaining on current prompt
                    #print(self.clock.tick_busy_loop())
                    prompt.update(self.clock.tick_busy_loop())
                    prompt.draw(self.win) #logic for checking whether still visible is inside prompt.draw
                    
                    #this one to ensure that pressing some other key doesn't break anything
                    if flag_responded: 
                        if flag_correct: #correct response
                            self.display_text("CORRECT", (self.disp_width/2,self.disp_height/3))
                        else:
                            self.display_text("WRONG", (self.disp_width/2,self.disp_height/3))

                    #check to see if respond time has been passed
                    if prompt.respondable_timer < 0:
                        
                        #if user did not provide a response, treat it as indicating no match
                        if not flag_responded:
                            result = self.game.store_response(0)
                            if result==False:
                                self.display_text("TOO SLOW/WRONG", (self.disp_width/2,self.disp_height/3))
                            else:
                                self.display_text("CORRECT", (self.disp_width/2,self.disp_height/3))
                        else:
                            if flag_correct:
                                self.display_text("CORRECT", (self.disp_width/2,self.disp_height/3))
                            else:
                                self.display_text("WRONG", (self.disp_width/2,self.disp_height/3))

                        #self.display_text("Waiting for next prompt...", (self.disp_width/2,self.disp_height/1.4))
                        pygame.display.update()
                        pygame.time.delay(500)


                        #get next prompt
                        val = self.game.get_next_prompt()
                        if val==None:
                            flag_game_complete = True
                            print(f"Completed Game #{self.trial.current_task-1}")
                            continue

                        prompt = Prompt(self.win, str(val), self.game.prompt_time_visible, self.game.prompt_time_respond)
                        flag_responded = False #only allow a single response per prompt
                        pygame.display.update()
                        self.clock.tick(30)
                        print(f"Displayed prompt {self.game.get_current_prompt_ind()}, value {val}, correcrt response {self.game.get_matches()[self.game.get_current_prompt_ind()-1]}")



                                    

            pygame.display.update()