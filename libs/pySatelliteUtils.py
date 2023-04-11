from AirCraft import * 
from Constants import *
import math

'''
[ Functions ]
 1. get_distance(AirCraft, AirCraft) -> float 
   Returns value of distance in Euclidian | UNIT -> [m]

 2. propagation_latency(AirCraft, AirCraft) -> float
   Returns value of propagation time | UNIT -> [s]

 3. 

'''

def get_distance(ac1: AirCraft, ac2: AirCraft) -> float: # Output : distance  UNIT -> [m]
    ac1_pos = ac1.get_position()
    ac2_pos = ac2.get_position()

    if(len(ac1_pos) == 2 and len(ac2_pos) == 2):
        return math.sqrt((ac1_pos[0] - ac2_pos[0])**2 + (ac1_pos[1] - ac2_pos[1])**2)
    
    elif(len(ac1_pos) == 3 and len(ac2_pos) == 3):
        return math.sqrt((ac1_pos[0] - ac2_pos[0])**2 + (ac1_pos[1] - ac2_pos[1])**2 + (ac1_pos[2] - ac2_pos[2])**2)

    else:
        if(len(ac1_pos) != 2 or len(ac1_pos) != 3 or len(ac2_pos) != 2 or len(ac2_pos) != 3):
            raise "Position length should be 2 or 3!!! ac1 size -> " + len(ac1_pos) + "ac2 size -> " + len(ac2_pos)

        if(len(ac1_pos) != len(ac2_pos)):
            raise "Length is Different! ac1 size -> " + len(ac1_pos) + "ac2 size -> " + len(ac2_pos)

def propagation_latency(src: AirCraft, dst: AirCraft) -> float: # Output : latency time  UNIT -> [s]
    return get_distance(src, dst) / C

def get_points_on_earth(d: float, num_points: int) -> list:
    _points = []
    _theta_gap = 2 * math.pi / num_points  # For regular interval # 일정한 간격

    for i in range(num_points):
        theta = i * _theta_gap
        x = d * math.cos(theta)
        y = d * math.sin(theta)
        _points.append((x, y))

    return _points

def get_velocities_on_earth(locations: list) -> list:

    _locations = []
    theta_gap = 2 * math.pi / len(locations)  # For regular interval # 일정한 간격

    return _locations


def get_relative_velocity_list(ac1: AirCraft, los: list):
    rv_list = []

    # for layer_idx, orbit in enumerate(los):  
    #     for sat_idx, sat in enumerate(orbit):
    #         # print(sat.get_position())
    #         # print("LAYER : ", layer_idx, "SAT ", sat_idx, " ==> ", sat.get_position())
    #         if(is_line_of_sight(ac1, sat)):
    #             line_of_sight_list.append((layer_idx, sat_idx))

    # return line_of_sight_list


########################################################################################
# ABOUT LINE OF SIGHT START
########################################################################################
def get_angle(x1, y1, x2, y2) -> float:
    # print(f"x1 => {x1}, y1 => {y1}, x2 => {x2}, y2 => {y2}")
    if((x1 == x2) and (y1 == y2)):
        return 0    
    
    r1 = math.sqrt((x1-EARTH_CENTER_LOC[0])**2 + (y1-EARTH_CENTER_LOC[1])**2)
    r2 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    r3 = math.sqrt((x2-EARTH_CENTER_LOC[0])**2 + (y2-EARTH_CENTER_LOC[1])**2)

    cos_theta = (r1**2 + r2**2 - r3**2) / (2 * r1 * r2) 

    if(cos_theta > 1):
        cos_theta = 1
    elif(cos_theta < -1):
        cos_theta = -1
    
    try:
        theta = math.acos(cos_theta)
    except Exception as e:
        print(e)
        print(cos_theta)

    degree = theta * 180 / math.pi
    return degree

def is_line_of_sight(ac1: AirCraft, ac2: AirCraft) -> bool:
    _alt = ac1.get_altitude()
    _theta = math.asin( R / _alt)
    _minimum_angle = (_theta * 180) / PI
    
    _x1, _y1 = ac1.get_position()[:2]
    _x2, _y2 = ac2.get_position()[:2]

    _angle = get_angle(_x1, _y1, _x2, _y2)

    # print("MINIMUM ANGLE => ", _minimum_angle, "CURRENT ANGLE => ", _angle)

    return abs(_angle) > _minimum_angle

def get_line_of_sight_list(ac1: AirCraft, orbits) -> list:
    line_of_sight_list = []
    for layer_idx, orbit in enumerate(orbits):  
        for sat_idx, sat in enumerate(orbit):
            # print(sat.get_position())
            # print("LAYER : ", layer_idx, "SAT ", sat_idx, " ==> ", sat.get_position())
            if(is_line_of_sight(ac1, sat)):
                line_of_sight_list.append((layer_idx, sat_idx))

    return line_of_sight_list

########################################################################################
# ABOUT LINE OF SIGHT END
########################################################################################



########################################################################################
# ABOUT CHANNEL LOSS START
########################################################################################

def free_space_path_loss(distance, velocity, propagation_velocity_angle: int =0):
    _term1 = 20 * math.log10(distance)
    _term2 = 20 * math.log10(FREQUENCY * velocity * math.cos(propagation_velocity_angle) / C)
    _term3 = 20 * math.log10(4 * PI / C)
    fspl = _term1 + _term2 + _term3

    return fspl

########################################################################################
# ABOUT CHANNEL LOSS END
########################################################################################



########################################################################################
# ABOUT CHANNEL CAPACITY START
########################################################################################

def channel_capacity(transmit_power, distance, velocity, propagation_velocity_angle):
    _Pr = transmit_power - free_space_path_loss(distance=distance, velocity=velocity, propagation_velocity_angle=propagation_velocity_angle)
    _Pn = -174 + 10*math.log(BAND_WIDTH)
    _snr = _Pr-_Pn
    return BAND_WIDTH * math.log2(1+_snr)

########################################################################################
# ABOUT CHANNEL CAPACITY END
########################################################################################


