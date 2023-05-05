import math
from libs.Constants import *
from libs.SimulationObject import *

class GroundUser(SimulationObject):
    def __init__(self,
                 pos: tuple = (0, 0, 0),
                 velocity: tuple = (0, 0, 0),
                 mass: int = 0):
        super().__init__(pos, velocity, mass)

        self.connected_sat = (1, 0)

    
    def reset(self):
        pass 

    def get_altitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)