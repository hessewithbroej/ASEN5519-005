import pygame
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

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

        #game results
        self.responses = -1*np.ones(num_prompts)
        self.successes = None
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

    def play_game(self):

        for i,prompt in enumerate(self.prompts):
            print(str(prompt))
            response = input("Enter 1 if prompt is the same as the prompt shown %d prompts prior, 0 otherwise: " % (self.N))
            self.responses[i] = int(response)
            if self.matches[i] == int(response):
                print("Correct!")
            else:
                print("Incorrect!")
        
        self.successes = self.responses == self.matches
        self.accuracy = float(self.successes.sum())/float(len(self.successes))
        self.report_results()
                
    def report_results(self):
        print(f"Test Results : \n {sum(self.successes)} correct reponses out of {self.num_prompts} total prompts. Overall accuracy: {100*self.accuracy} %")

