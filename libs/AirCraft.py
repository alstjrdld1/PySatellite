import math

from libs.Constants import *
from libs.SimulationObject import *

class AirCraft(SimulationObject):
    '''
    ---------------------------------------------
    |position           : m      [meter]         |
    |velocity           : m/s    [meter/second]  |
    |altitude           : m      [meter]         |
    |mass               : kg     [kilogram]      |
    |computing resource :        [        ]      | considering
    ---------------------------------------------
    '''
    def __init__(self, 
                 pos: tuple = (0, 0, 0),
                 velocity: tuple = (0, 0, 0),
                 mass: int = 0):
        
        super().__init__(pos, velocity, mass)

    def get_altitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
class Satellite(AirCraft):
    def __init__(self,
                 pos:       tuple = (0,0,0),
                 velocity:  tuple = (0,0,0),
                 mass:      int = 0,
                 task_num : int = 5):
        super().__init__(pos, velocity, mass)

        self.tasks = [0 for i in range(task_num)] # 0 -> Empty 1 -> Ocuupied

    def get_tasks(self):
        return self.tasks

class UAV(AirCraft):
    def __init__(self,
                 pos: tuple = (0,0,0),
                 velocity: tuple = (0,0,0),
                 mass: int = 0):
        super().__init__(pos, velocity, mass)