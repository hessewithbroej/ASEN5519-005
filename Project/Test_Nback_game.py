import unittest
import Nback_game as nbg
import numpy as np

class Test_Nback_game(unittest.TestCase):

    #wip
    def test_grading(self,N):
        game = nbg.Nback_game(N, 20, 5, 0.25)
        game.set_prompts = np.asarray([15, 99, 15, 15, 89, 79, 15, 99, 69, 59, 15, 15, 15, 99, 89, 15, 79, 15, 69, 15])
        if N == 1:
            game.set_matches = np.asarray([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0])
        elif N==2:
            game.set_matches = np.asarray([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1])
        elif N==3:
            game.set_matches = np.asarray([0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
        elif N==4:
            game.set_matches = np.asarray([0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1])
        else:
            raise Exception("Unit testing for N>4 currently not supported")
        
        game.set_responses = np.asarray([0])