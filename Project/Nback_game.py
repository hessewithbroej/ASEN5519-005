import pygame
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
from Manager import *

class Nback_game:

    TWO_DIGIT_INTEGERS = range(10,100)

    def __init__(self, N, num_prompts, proportion_true, prompt_time_visible, prompt_time_respond):
        #game conditions, general
        self.num_prompts = num_prompts
        self.N = N
        self.proportion_true = proportion_true
        self.prompt_time_visible = prompt_time_visible
        self.prompt_time_respond = prompt_time_respond

        #game conditions, specific
        self.prompts = None
        self.matches = np.zeros(num_prompts)

        #live game variables
        self.current_prompt = 0
        self.responses = np.asarray([])

        #game results
        self.successes = np.asarray([])
        self.accuracy = None

        self.generate_prompts()

    def get_prompts(self):
        return self.prompts
    
    def get_responses(self):
        return self.responses
    
    def get_successes(self):
        return self.successes
    
    def get_matches(self):
        return self.matches
    
    def get_accuracy(self):
        return self.accuracy
    
    def set_prompts(self, prompts):
        self.prompts = prompts

    def set_matches(self, matches):
        self.matches = matches

    def set_responses(self, responses):
        self.responses = responses
    
    def set_successes(self, successes):
        self.successes = successes
    
    def set_accuracy(self,accuracy):
        self.accuracy = accuracy


    def generate_prompts(self):
        #Generates the list of prompts to be provided to the participant

        #generate a list of num_prompts random 2-digit numbers and 
        #ensure none initially satisfy the N-back condition by sampling without replacement
        self.prompts = np.random.choice(self.TWO_DIGIT_INTEGERS,self.num_prompts, replace=False)

        #number of prompts satisfying the specified N-back condition
        #the first N responses can't be true by nature of the game
        num_true = int(np.ceil((self.num_prompts-self.N)*self.proportion_true))

        #generate a list that contains the prompt numbers that should evaluate to true
        true_indices = np.sort(np.random.choice(range(self.N,self.num_prompts), num_true, replace=False))[::-1]

        #replace prompts so that the correct response is true for the above indices
        #need to replace from the back of the list to the front so we don't overwrite 
        #previously-updated prompts
        for i,ind in enumerate(true_indices):
            self.prompts[ind-self.N] = self.prompts[ind]
            self.matches[ind] = 1

    #sets up the pygame contained in the Manager class
    # def setup_game(self):
        # pygame_mgr = Manager(self)
        # pygame_mgr.gameloop()

    #helper function return for commandline outputs
    def get_current_prompt_ind(self):
        return(self.current_prompt)

    #get the next prompt in the sequence of prompts
    def get_next_prompt(self):
        if self.current_prompt < self.num_prompts:
            ind = self.current_prompt
            self.current_prompt += 1
            return(self.prompts[ind])
        else:
            print("Game complete.")
            self.report_results()
            return(None)

    def store_response(self, response):
        #store response (0 or 1) in responses array
        self.responses = np.append(self.get_responses,response)
        #store wheter response was correct in successess array
        self.successes = np.append(self.successes, response==self.matches[self.get_current_prompt_ind()-1])

        #return whether result was correct so it can  be displayed
        return(response==self.matches[self.get_current_prompt_ind()-1])


    def report_results(self):
        self.accuracy = sum(self.successes)/self.num_prompts
        print(f"Test Results : \n {sum(self.successes)} correct reponses out of {self.num_prompts} total prompts. Overall accuracy: {100*self.accuracy} %")

