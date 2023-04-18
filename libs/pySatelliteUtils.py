from .AirCraft import * 
from .Constants import *

from typing import List
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
    _term1 = (ac1_pos[0] - ac2_pos[0])**2
    _term2 = (ac1_pos[1] - ac2_pos[1])**2
    _term3 = (ac1_pos[2] - ac2_pos[2])**2
    return math.sqrt( _term1 + _term2 + _term3 )

########################################################################################
# ABOUT PROPAGATION START 
########################################################################################
def propagation_latency(src: AirCraft, dst: AirCraft) -> float: # Output : latency time  UNIT -> [s]
    return get_distance(src, dst) / C

def get_propagation_angle(src_ac: AirCraft, dst_ac: AirCraft) -> float : # Output : Radian
    src_pos = src_ac.get_position()
    dst_pos = dst_ac.get_position()

    _propagate_vector = (dst_pos[0] - src_pos[0], dst_pos[1] - src_pos[1], dst_pos[2] - src_pos[2])
    # print(_propagate_vector)
    _velocity_vector = src_ac.get_velocity()
    # print(_velocity_vector)
    
    _dot_prod = sum([_propagate_vector[i] * _velocity_vector[i] for i in range(3)])
    _mag1 = math.sqrt(sum([_propagate_vector[i]**2 for i in range(3)]))
    _mag2 = math.sqrt(sum([_velocity_vector[i]**2 for i in range(3)]))

    if(_mag1 == 0 or _mag2 == 0):
        return 0
    _cos_theta = _dot_prod / (_mag1*_mag2)
    if _cos_theta < -1:
        _cos_theta = -1
    elif _cos_theta > 1 :
        _cos_theta = 1
    
    try:
        _angle = math.acos(_cos_theta)
    except Exception as e :
        print (e)
        print(_dot_prod)
        print(_mag1)
        print(_mag2)
        raise 

    return _angle

def get_propagation_angle_list(dst_ac:AirCraft, sats:List[List[AirCraft]], los_list:List[List[bool]]) -> list:
    _prop_angles = []    
    for orbit_idx, orbit in enumerate(los_list):
        _prop_row = []
        for sat_idx, sat_is_visible in enumerate(orbit):
            if(sat_is_visible):
                _prop_angle = get_propagation_angle(sats[orbit_idx][sat_idx], dst_ac)
                _prop_row.append(_prop_angle)
            else:
                _prop_row.append(0)
        _prop_angles.append(_prop_row)
    return _prop_angles
########################################################################################
# ABOUT PROPAGATION START 
########################################################################################





########################################################################################
# ABOUT INITIALIZATION START
########################################################################################
def get_points_on_earth(d: float, num_points: int) -> list:
    _points = []
    _theta_gap = 2 * math.pi / num_points  # For regular interval # 일정한 간격

    for i in range(num_points):
        theta = i * _theta_gap
        x = d * math.cos(theta)
        y = d * math.sin(theta)
        # print("THEATA => ", theta, "X => ", x, "Y => ", y)
        _points.append((x, y))

    return _points

def get_angular_velocity(altitude: float) -> float:
    return math.sqrt(G * M / (altitude) ** 3)
########################################################################################
# ABOUT INITIALIZATION END
########################################################################################




########################################################################################
# ABOUT RELATIVE VELOCITY START
########################################################################################
def get_relative_velocity(ac1: AirCraft, ac2: AirCraft) -> tuple:
    _v1x, _v1y, _v1z = ac1.get_velocity()
    _v2x, _v2y, _v2z = ac2.get_velocity()
    return (_v1x - _v2x, _v1y - _v2y, _v1z - _v2z)

def get_relative_velocity_list(ac1: AirCraft, sats: List[List[AirCraft]], visible_list: List[List[bool]]) -> list:
    _rvs = []    
    for orbit_idx, orbit in enumerate(visible_list):
        _rv_row = []
        for sat_idx, is_visible in enumerate(orbit):
            if(is_visible):
                _rv = get_relative_velocity(ac1, sats[orbit_idx][sat_idx])
                _rv_row.append(_rv)
            else:
                _rv_row.append((0,0,0))
        _rvs.append(_rv_row)
    return _rvs
########################################################################################
# ABOUT RELATIVE VELOCITY END
########################################################################################





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
    if(abs(_angle) < 0.001 and get_distance(ac1, ac2) < R):
        return True
    
    return abs(_angle) > _minimum_angle

def get_line_of_sight_list(ac1: AirCraft, orbits) -> list:
    _los_orbits = []
    for orbit in orbits:  
        _los_orbit = []
        for sat in orbit:
            # print(sat.get_position())
            # print("LAYER : ", layer_idx, "SAT ", sat_idx, " ==> ", sat.get_position())
            if(is_line_of_sight(ac1, sat)):
                _los_orbit.append(True)
            else: 
                _los_orbit.append(False)
        _los_orbits.append(_los_orbit)

    return _los_orbits
########################################################################################
# ABOUT LINE OF SIGHT END
########################################################################################



########################################################################################
# ABOUT CHANNEL LOSS START
########################################################################################
def free_space_path_loss(distance, velocity, propagation_velocity_angle: int =0):

    # print("DISTANCE : ", distance, "VELOCITY : ", velocity, "PROP VEL ANGLE : ", propagation_velocity_angle)
    
    _term1 = 20 * math.log10(distance)
    # print("_TERM1 : ", _term1)
    _f_r = FREQUENCY * velocity * abs(math.cos(propagation_velocity_angle) / C)
    # print("_F_R : ", _f_r)
    _term2 = 20 * math.log10(_f_r)
    # print("_TERM2 : ", _term2)
    _term3 = 20 * math.log10(4 * PI / C)
    # print("_TERM3 : ", _term3)

    fspl = _term1 + _term2 + _term3

    return fspl
########################################################################################
# ABOUT CHANNEL LOSS END
########################################################################################

def get_snr(distance, velocity, velocity_angle):
    _freq = FREQUENCY * velocity  * abs(math.cos(velocity_angle) / C)
    _Pr = (TRANSMISSION_POWER * (ANTENNA_EFFICIENCY**2) * (PI**2) * (ANTENNA_DIAMETER**4) * (_freq**2)) / (16 * (C **2) * (distance**2))
    _snr = _Pr / (ADDITIONAL_NOISE_RECEIVER*BOLTZMAN_CONSTANT*TEMPERATURE*BAND_WIDTH)
    return _snr

########################################################################################
# ABOUT CHANNEL CAPACITY START
########################################################################################
def channel_capacity(transmit_power, distance, velocity, propagation_velocity_angle):
    # if(distance < 1):
    #     distance = 1
    # _Pr = transmit_power - free_space_path_loss(distance=distance, velocity=velocity, propagation_velocity_angle=propagation_velocity_angle)
    # print("_Pr : ", _Pr)
    
    # _Pn = -174 + 10*math.log(BAND_WIDTH)
    # print("_Pn : ", _Pn)

    # _snr = _Pr - _Pn
    # if(_snr < -1):
    #     return 1
    _snr = get_snr(distance, velocity, propagation_velocity_angle)
    
    return BAND_WIDTH * math.log2(1+_snr)
########################################################################################
# ABOUT CHANNEL CAPACITY END
########################################################################################