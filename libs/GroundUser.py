import math
from libs.Constants import *
from libs.SimulationObject import *
from libs.AirCraft import *

class GroundUser(SimulationObject):
    def __init__(self,
                 pos: tuple = (0, 0, 0),
                 velocity: tuple = (0, 0, 0),
                 mass: int = 0):
        super().__init__(pos, velocity, mass)

        self.connected_sat = (0, 0)
        self.prev_connected_sat = (0, 0)

    def reset(self):
        pass 

    def get_velocity(self) -> tuple:
        current_angle = self.get_current_angle()

        vx = EARTH_SURFACE_ROTATE_SPEED * math.sin(current_angle)
        vy = EARTH_SURFACE_ROTATE_SPEED * math.cos(current_angle)
        vz = 0
        return [vx, vy, vz]

    def get_altitude(self) -> float:
        return 6371
    
    def calc_relative_velocity(self, obj:SimulationObject):
        mvx, mvy, mvz = self.get_velocity()
        ovx, ovy, ovz = obj.get_velocity()
        return mvx - ovx, mvy - ovy, mvz - ovz
    
    def get_connected_sat(self):
        return self.connected_sat
    
    def get_prev_connected_sat(self):
        return self.prev_connected_sat
    
    def set_connected_sat(self, new_sat: tuple = (-1, -1)) -> None:
        self.prev_connected_sat = self.connected_sat
        self.connected_sat = new_sat
