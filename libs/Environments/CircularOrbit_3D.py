from abc import abstractmethod
from libs.Environments.OrbitBaseline import *

class CircularOrbit_3D(OrbitBaseLine):
    def __init__(self,
                 satellite_num: int = 8,
                 orbit_alts: list =[400, 1000]):
        
        super.__init__(satellite_num = satellite_num,
                       orbit_alts = orbit_alts)
        pass 
    
    @abstractmethod
    def reset(self) -> None:
        pass 

    @abstractmethod
    def get_reward(self) -> float:
        pass

    @abstractmethod
    def step(self, action):
        pass 

    @abstractmethod
    def set_action(self, action: int) -> list:
        pass

    @abstractmethod
    def get_state(self):
        pass
    
    def los(self) -> list:
        pass 

    def rotate(self, t) -> None:
        pass

    def plot(self) -> None:
        pass