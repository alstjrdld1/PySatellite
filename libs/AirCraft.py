import math

class AirCraft:
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
        
        if(len(pos) != 3):
            raise "Position only have 2 or 3 dimension"
        
        if(len(velocity) != 3):
            raise "Velocity only have 2 or 3 dimension"
        
        self.initialize_position()
        self.initialize_velocity()

        self.set_position(pos)
        self.set_velocity(velocity)
        
        self.mass = mass
        self.altitude = pos[2]

    def initialize_position(self):
        self.x = 0 
        self.y = 0
        self.z = 0
    
    def initialize_velocity(self):
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def get_velocity(self) -> tuple:
        return (self.vx, self.vy, self.vz)

    def set_velocity(self,  velocity: tuple = (0,0)):
        if(len(velocity) == 3):
            self.vx, self.vy, self.vz = velocity
        else:
            raise "Velocity only have 2 or 3 dimension"
        
    def get_position(self) -> tuple:
        return (self.x, self.y, self.z) 
    
    def set_position(self, pos: tuple = (0, 0)):
        if(len(pos) == 3):
            self.x, self.y, self.z = pos
        else:
            raise "Position only have 2 or 3 dimension"

    def get_altitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
class Satellite(AirCraft):
    def __init__(self,
                 pos: tuple = (0,0,0),
                 velocity: tuple = (0,0,0),
                 mass: int = 0):
        super().__init__(pos, velocity, mass)

class UAV(AirCraft):
    def __init__(self,
                 pos: tuple = (0,0,0),
                 velocity: tuple = (0,0,0),
                 mass: int = 0):
        super().__init__(pos, velocity, mass)