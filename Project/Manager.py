import pygame
import sys
import Nback_game as nbg
from Prompt import *
from Trial import *
from Autologger import *
from datetime import datetime


class Manager:
    pygame.font.init()
    DEFAULT_FONT = pygame.font.Font('freesansbold.ttf',32)

    def __init__(self, trial, disp_width = 800, disp_height = 800):
        self.trial = trial
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
        
        user_text = '' 
        flag_ID_generated = False
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
                            # seconds = 3
                            # for i in range(seconds+1):
                            #     self.win.fill((255, 255, 255))
                            #     text_string = f"Test Beginning in {seconds-i} seconds..."
                            #     self.display_text(text_string, (self.disp_width/2,self.disp_height/1.6))
                            #     pygame.display.update()
                            #     pygame.time.delay(1000)
                            self.game_phase = "info_enter"
            
            elif self.game_phase == "info_enter":
                self.display_text("If this is your first trial, press J.", (self.disp_width/2,self.disp_height/1.6))
                self.display_text("Otherwise, enter your 5-digit ID # and press Enter.", (self.disp_width/2,self.disp_height/1.4))

                # create rectangle 
                self.display_text("ID: ", (360,616))
                input_rect = pygame.Rect(self.disp_width/2, 600, 140, 32) 
                
                # color_active stores color(lightskyblue3) which 
                # gets active when input box is clicked by user 
                color_active = pygame.Color('lightskyblue3') 
                color = color_active 

                for event in pygame.event.get():
                    #quit game when forced
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_j:
                                self.game_phase = "id_assignment"



                        elif event.key == pygame.K_BACKSPACE:
                            #only allow backspacing if some text already exists
                            if user_text:
                                user_text = user_text[:-1]

                        elif event.unicode.isdigit() and len(user_text) < 5:
                            user_text = user_text + event.unicode
                            

                        elif event.key == pygame.K_RETURN:
                            if len(user_text) == 5:
                                ID = np.asarray([int(user_text)])
                                #get group number and trial number from trialKey spreadsheet to determine the task sequence
                                group_number, trial_num = Autologger.find_previous_trial_results(Autologger.read_trial_data_from_sheet(), ID)
                                task_sequence = Autologger.determine_next_trial(group_number, trial_num)

                                if task_sequence == None:
                                    self.win.fill((255, 255, 255))
                                    self.display_text(f"All trials have been completed.", (self.disp_width/2,self.disp_height/1.8))
                                    self.display_text(f"Thank you for participating.", (self.disp_width/2,self.disp_height/1.6))
                                    pygame.display.update()
                                    pygame.time.delay(3000)
                                    pygame.quit()
                                    sys.exit()

                                trial_num += 1
                                self.trial.task_sequence = str(task_sequence)
                                
                                
                                self.game_phase = "playing"
                            else:
                                self.display_text("Invalid ID #, must be 5 digits.", (self.disp_width/2,self.disp_height-300))


                    
                pygame.draw.rect(self.win, color, input_rect) 
                text_surface = self.DEFAULT_FONT.render(user_text, True, (255, 255, 255)) 
                # render at position stated in arguments 
                self.win.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
                pygame.display.update()

            elif self.game_phase == "id_assignment":
                if not flag_ID_generated:
                    ID = self.trial.generate_ID()
                    group_number = int(np.random.randint(1,24,1))
                    flag_ID_generated = True
                    print(f"Generated ID={ID}, assigned to group={group_number}")
                
                self.win.fill((255, 255, 255))
                self.display_text("Your unique ID # is: ", (self.disp_width/2,self.disp_height-600))
                self.display_text(str(ID), (self.disp_width/2,self.disp_height-550))
                self.display_text("RECORD THIS NUMBER IN A SAFE PLACE.", (self.disp_width/2,self.disp_height-500))
                self.display_text("YOU WILL NEED IT FOR FUTURE TESTS.", (self.disp_width/2,self.disp_height-450))
                self.display_text("When ready, press J to begin testing.", (self.disp_width/2,self.disp_height-400))
                pygame.display.update()

                #first trial for a new participant is control
                trial_num = 1
                self.trial.task_sequence = "222222"
                
                #check for keyboard input
                for event in pygame.event.get():
                    #quit game when forced
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    #look for user response
                    if event.type == pygame.KEYDOWN:

                        #user ready to begin testing
                        if event.key == pygame.K_j:
                            self.win.fill((255, 255, 255))
                            self.game_phase = "playing"
                            pygame.display.update()

            elif self.game_phase == "playing":
                
                #when user has answered all prompts in a given nback game/task, or its our first game
                if flag_game_complete or self.trial.current_task == 0:
                    if flag_game_complete:
                        
                        pygame.event.pump() #may help prevent lag/stuttering
                        #save the timestamp when task was completed
                        now = datetime.now()
                        task_complete_time = now.strftime("%m/%d/%Y %H:%M:%S")

                        self.win.fill((255, 255, 255))
                        self.display_text(f"Completed game number {self.trial.current_task} of {len(self.trial.task_sequence)}.", (self.disp_width/2,self.disp_height/1.8))
                        self.display_text(f"Overall Accuracy: {self.game.accuracy*100}%", (self.disp_width/2,self.disp_height/1.6))
                        pygame.display.update()

                        #write task-level data to sheet
                        Autologger.write_task_data_to_sheet(ID,group_number,trial_num, task_complete_time, self.trial.current_task, self.trial.game.N, self.trial.game.prompts, self.trial.game.matches, self.trial.game.responses, self.trial.game.successes, self.trial.game.accuracy)
                        self.trial.accuracies = np.append(self.trial.accuracies, self.trial.game.accuracy)
                        pygame.time.delay(4000)
                        pygame.event.pump()
                    
                    self.game = self.trial.serve_next_game()


                    #only show countdown when tasks remaining
                    if self.trial.current_task-1 < len(self.trial.task_sequence):


                        #if we've completed all tasks
                        if self.game == None:
                            self.win.fill((255, 255, 255))
                            self.display_text("All games in trial have been completed.", (self.disp_width/2,self.disp_height/1.8))
                            self.display_text("Exiting", (self.disp_width/2,self.disp_height/1.6))
                            
                            now = datetime.now()
                            trial_complete_time = now.strftime("%m/%d/%Y %H:%M:%S")

                            #write trial-level performance to sheet
                            Autologger.write_trial_data_to_sheet(ID, group_number, trial_num, trial_complete_time, self.trial.task_sequence, self.trial.accuracies)

                            pygame.display.update()
                            pygame.time.delay(5000)
                            pygame.quit()
                            sys.exit()

                        seconds = 3
                        for i in range(seconds+1):
                            pygame.event.pump()
                            self.win.fill((255, 255, 255))

                            text_string = f"Next task is N={self.trial.game.N}-back."
                            self.display_text(text_string, (self.disp_width/2,self.disp_height-600))

                            text_string = f"When the current prompt is equal to the prompt"
                            self.display_text(text_string, (self.disp_width/2,self.disp_height-550))
                            text_string = f"shown {self.trial.game.N} prompts previously, press J."
                            self.display_text(text_string, (self.disp_width/2,self.disp_height-515))

                            text_string = f"Prompts will be displayed for {float(self.trial.NBACK_PROMPT_TIME_VISIBLE)/1000.0} seconds, "
                            self.display_text(text_string, (self.disp_width/2,self.disp_height-465))        
                            text_string = f"you will have {float(self.trial.NBACK_PROMPT_TIME_RESPONDABLE)/1000.0} seconds to respond."
                            self.display_text(text_string, (self.disp_width/2,self.disp_height-430))          
                            # text_string = f"When no inpu"
                            # self.display_text(text_string, (self.disp_width/2,self.disp_height-435))              

                            text_string = f"Next task begins in {seconds-i} seconds..."
                            self.display_text(text_string, (self.disp_width/2,self.disp_height-300))

                            pygame.display.update()
                            pygame.time.delay(1000)

                    flag_game_complete = False

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

                            #user suspects no match
                            if event.key == pygame.K_f and not flag_responded:
                                result = self.game.store_response(0)
                                flag_responded = True
                                flag_correct = result
                

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
                        print(f"Displayed prompt {self.game.get_current_prompt_ind()}, value {val}, correct response {self.game.get_matches()[self.game.get_current_prompt_ind()-1]}")



                                    

            pygame.display.update()