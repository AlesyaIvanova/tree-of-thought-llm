import re
import os
import sympy
import pandas as pd
from tot.tasks.base import Task, DATA_PATH
from tot.prompts.connections import * 


# def get_current_numbers(y: str) -> str:
#     last_line = y.strip().split('\n')[-1]
#     return last_line.split('left: ')[-1].split(')')[0]


class Connections(Task):
    # """
    # Input (x)   : a string of 4 numbers
    # Output (y)  : a trajectory of 3 steps to reach 24
    # Reward (r)  : 0 or 1, depending on whether the trajectory is correct
    # Input Example: 
    #     1 2 3 4
    # Output Example: 
    #     1 + 2 = 3 (left: 3 3 4)
    #     3 + 3 = 6 (left: 4 6)
    #     6 * 4 = 24 (left: 24)
    #     (1 + 2 + 3) * 4 = 24
    # """
    def __init__(self, file='connections.csv'):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        path = os.path.join(DATA_PATH, 'connections', file)
        self.data = list(pd.read_csv(path))
        self.value_cache = {}
        self.steps = 4
        self.stops = ['\n'] * 4

    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        input = self.data[idx]['clue1'] + "\n---\n" \
        + self.data[idx]['clue2'] + "\n---\n" \
        + self.data[idx]['clue3'] + "\n---\n" \
        + self.data[idx]['clue4'] + "\n---\n"

    def test_output(self, idx: int, output: str):
        if output == self.data[idx]["answer"]: # TODO
          return {'r': 1}
        return {'r': 0}
            
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x)
    
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        prompt = propose_prompt.format(input=x, output=y)
        return prompt
    
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        return value_prompt.format(input=x, output=y)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value