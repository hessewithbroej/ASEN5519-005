import Nback_game as nbg
import Manager as mgr
from Autologger import *
import numpy as np


class Trial:

    NBACK_NUM_PROMPTS = 20
    NBACK_PROP_MATCH = 0.25
    NBACK_PROMPT_TIME_VISIBLE = 0.5
    NBACK_PROMPT_TIME_RESPONDABLE = 3000
    MIN_TIME_BETWEEN_TRIALS = 86400*1000

    def __init__(self, task_sequence, current_task=0):
        self.task_sequence = task_sequence
        self.current_task = current_task
        self.game_active = False
        self.game = None
        self.accuracies = np.asarray([])

    #generate a unique ID number that has not already been assigned to another participant
    @classmethod
    def generate_ID(self):
        df = Autologger.read_trial_data_from_sheet()
        taken_IDs = df.ID.unique()
        taken_IDs = np.append(taken_IDs,[11111,12345,10000])
        #generate a unique ID
        while True:
            ID = np.random.randint(low = 10000, high = 20000, size = 1)
            if ID not in taken_IDs:
                break
        return(ID)

    #begin a series of NBACK tasks
    def start_trial(self):
        pygame_mgr = mgr.Manager(self)
        pygame_mgr.gameloop()

    #start the next NBACK game in the task sequence
    def serve_next_game(self):
        if self.current_task < len(self.task_sequence):
            N = int(self.task_sequence[self.current_task])
            self.current_task += 1
            self.game_active = True
            self.game = nbg.Nback_game(N, self.NBACK_NUM_PROMPTS, self.NBACK_PROP_MATCH, self.NBACK_PROMPT_TIME_VISIBLE, self.NBACK_PROMPT_TIME_RESPONDABLE)
            return(self.game)
        else:
            self.end_game()
            return(None)

    #end the game
    def end_game(self):
        self.game_active = False

        