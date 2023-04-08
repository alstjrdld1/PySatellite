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
                 pos: tuple = (0,0),
                 velocity: tuple = (0,0),
                 altitude: float = 0.0,
                 mass: int = 0):
        
        if(len(pos) == 2 or len(pos) == 3):
            pass
        else:
            raise "Position only have 2 or 3 dimension"
        
        if(len(velocity) == 2 or len(velocity) == 3):
            pass
        else:
            raise "Velocity only have 2 or 3 dimension"

        self.initialize_position(pos)
        self.initialize_velocity(velocity)
        
        self.mass = mass
        self.altitude = altitude

    def initialize_position(self, pos: tuple = (0, 0)):
        if(len(pos) == 2):
            self.x, self.y = pos
        elif(len(pos) == 3):
            self.x, self.y, self.z = pos
    
    def initialize_velocity(self, velocity: tuple = (0,0)):
        if(len(velocity) == 2):
            self.vx, self.vy = velocity
        elif(len(velocity) == 3):
            self.vx, self.vy, self.vz = velocity

    def get_velocity(self) -> tuple:
        try:
            return (self.vx, self.vy, self.vz)
        except:
            return (self.vx, self.vy)
    
    def get_position(self) -> tuple:
        try:
            return (self.x, self.y, self.z)
        except:
            return (self.x, self.y)
        
    def update_velocity(self, vx, vy):
        self.vx = vx
        self.vy = vy
    
    def update_position(self, x, y):
        self.x = x
        self.y = y

class Satellite(AirCraft):
    def __init__(self,
                 pos: tuple = (0,0),
                 velocity: tuple = (0,0),
                 altitude: float = 0.0,
                 mass: int = 0):
        super().__init__(pos, velocity, altitude, mass)

class UAV(AirCraft):
    def __init__(self,
                 pos: tuple = (0,0),
                 velocity: tuple = (0,0),
                 altitude: float = 0.0,
                 mass: int = 0):
        super().__init__(pos, velocity, altitude, mass)