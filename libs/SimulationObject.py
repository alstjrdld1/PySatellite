import math
from abc import abstractmethod, ABC

from libs.Constants import *

class SimulationObject(ABC):
    def __init__(self,
                 pos: tuple = (0, 0, 0),
                 velocity: tuple = (0, 0, 0),
                 mass: int = 0):
        
        if(len(pos) != 3):
            raise "Position have to be 3 dimension"
        
        if(len(velocity) != 3):
            raise "Velocity have to be 3 dimension"
        
        self.initialize_position()
        self.initialize_velocity()

        self.set_position(pos)
        self.set_velocity(velocity)
        
        self.mass = mass
        self.altitude = self.get_altitude()

        self.angular_velocity = math.sqrt(G * M / (self.altitude) ** 3)
    
    def initialize_position(self):
        self.x = 0 
        self.y = 0
        self.z = 0
    
    def initialize_velocity(self):
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def get_angular_velocity(self):
        return self.angular_velocity

    def get_current_angle(self):
        if(self.x == 0):
            self.x = 0.0000000000001
        _angle = math.atan2( (self.y - EARTH_CENTER_LOC[1]) , (self.x - EARTH_CENTER_LOC[0]))
        
        # print(f"{(_angle * 180 / PI):.4f}")
        return float(f"{_angle:.4f}")

    def get_velocity(self) -> tuple:
        r = self.get_altitude()
        r = r * 1000

        v = math.sqrt((G * M) / r) / 1000 # -> m / s

        _theta = self.get_current_angle()
        self.vx = v * math.sin(_theta)
        self.vy = v * math.cos(_theta)
        self.vz = 0

        return [self.vx, self.vy, self.vz]
    
    def get_velocity_mag(self) -> float:
        _vx, _vy, _vz = self.get_velocity()
        return math.sqrt(_vx**2 + _vy**2 + _vz**2)

    def set_velocity(self,  velocity: tuple = (0, 0, 0)):
        if(len(velocity) == 3):
            self.vx = float(f"{velocity[0]:.4f}")
            self.vy = float(f"{velocity[1]:.4f}")
            self.vz = float(f"{velocity[2]:.4f}")
        else:
            raise "Velocity only have 2 or 3 dimension"
        
    def get_position(self) -> tuple:
        return [self.x, self.y, self.z]
    
    def set_position(self, pos: tuple = (0, 0, 0)):
        if(len(pos) == 3):
            self.x = float(f"{pos[0]:.4f}")
            self.y = float(f"{pos[1]:.4f}")
            self.z = float(f"{pos[2]:.4f}")
        else:
            raise "Position only have 2 or 3 dimension"

    def get_altitude(self) -> float:
        print("X :", self.x)
        print("Y :", self.y)
        print("Z :", self.z)
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
