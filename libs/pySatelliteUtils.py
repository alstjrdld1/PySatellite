from .AirCraft import * 
from .Constants import *
from .GroundUser import *

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

def get_distance(ac1: SimulationObject, ac2: SimulationObject) -> float: # Output : distance  UNIT -> [m]
    ac1_pos = ac1.get_position()
    ac2_pos = ac2.get_position()
    _term1 = (ac1_pos[0] - ac2_pos[0])**2
    _term2 = (ac1_pos[1] - ac2_pos[1])**2
    _term3 = (ac1_pos[2] - ac2_pos[2])**2
    return math.sqrt( _term1 + _term2 + _term3 ) * 1e-5

########################################################################################
# ABOUT PROPAGATION START 
########################################################################################
def propagation_latency(src: SimulationObject, dst: SimulationObject) -> float: # Output : latency time  UNIT -> [s]
    return 1e5 * get_distance(src, dst) / C

def get_propagation_angle(src_ac: SimulationObject, dst_ac: SimulationObject) -> float : # Output : Radian
    src_pos = src_ac.get_position()
    dst_pos = dst_ac.get_position()

    _propagate_vector = (dst_pos[0] - src_pos[0], dst_pos[1] - src_pos[1], dst_pos[2] - src_pos[2])
    # _propagate_vector = (src_pos[0] - dst_pos[0], src_pos[1] - dst_pos[1], src_pos[2] - dst_pos[2])
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

def get_propagation_angle_list(dst_ac:SimulationObject, sats:List[List[SimulationObject]], los_list:List[List[bool]]) -> list:
    _prop_angles = []    
    for orbit_idx, orbit in enumerate(los_list):
        _prop_row = []
        for sat_idx, sat_is_visible in enumerate(orbit):
            if(sat_is_visible == 1):
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
def get_relative_velocity(ac1: SimulationObject, ac2: SimulationObject) -> tuple:
    _v1x, _v1y, _v1z = ac1.get_velocity()
    _v2x, _v2y, _v2z = ac2.get_velocity()
    # return (_v1x - _v2x, _v1y - _v2y, _v1z - _v2z)
    return (_v2x - _v1x, _v2y - _v1y, _v2z - _v1z)

def get_relative_velocity_list(ac1: SimulationObject, sats: List[List[SimulationObject]], visible_list: List[List[bool]]) -> list:
    _rvs = []    
    for orbit_idx, orbit in enumerate(visible_list):
        _rv_row = []
        for sat_idx, is_visible in enumerate(orbit):
            if(is_visible == 1):
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

def is_line_of_sight(ac1: SimulationObject, ac2: SimulationObject) -> bool:

    _alt = ac1.get_altitude()
    _theta = math.asin( R / _alt)
    _minimum_angle = (_theta * 180) / PI
    
    _x1, _y1 = ac1.get_position()[:2]
    _x2, _y2 = ac2.get_position()[:2]
    
    if((_x1 == _x2) and (_y1 == _y2)):
        return False

    _angle = get_angle(_x1, _y1, _x2, _y2)

    # print("MINIMUM ANGLE => ", _minimum_angle, "CURRENT ANGLE => ", _angle)
    if(abs(_angle) < 0.001 and 1e5*get_distance(ac1, ac2) < R):
        return True
    
    return abs(_angle) > _minimum_angle
def get_line_of_sight_list_tf(ac1: AirCraft, orbits) -> list:
    _los_orbits = []
    for orbit in orbits:  
        _los_orbit = []
        for sat in orbit:
            if(is_line_of_sight(ac1, sat)):
                _los_orbit.append(True)
            else: 
                _los_orbit.append(False)
        _los_orbits.append(_los_orbit)

    return _los_orbits
'''
def get_line_of_sight_list(ac1: SimulationObject, srcsat:SimulationObject, dstsat:SimulationObject, orbits) -> list:
    _los_orbits = []
    for orbit in orbits:  
        _los_orbit = []
        for sat in orbit:
            if(dstsat.get_position() == sat.get_position()):
                _los_orbit.append(2)
            elif(ac1.get_position() == sat.get_position()):
                _los_orbit.append(1)
            # print(sat.get_position())
            # print("LAYER : ", layer_idx, "SAT ", sat_idx, " ==> ", sat.get_position())
            else:
                if(is_line_of_sight(ac1, sat)):
                    _los_orbit.append(3)
                else: 
                    _los_orbit.append(0)
        _los_orbits.append(_los_orbit)

    return _los_orbits
'''

def get_line_of_sight_list(ac1: SimulationObject, orbits) -> list:
    _los_orbits = []
    for orbit in orbits:  
        _los_orbit = []
        for sat in orbit:
            if(is_line_of_sight(ac1, sat)):
                _los_orbit.append(1)
            else: 
                _los_orbit.append(0)
        _los_orbits.append(_los_orbit)

    return _los_orbits
########################################################################################
# ABOUT LINE OF SIGHT END
########################################################################################

def get_computing_resources(los_list: list, orbits) -> list:
    s_comp = []
    for l, layer in enumerate(los_list):
        layer_comp = []
        for i, index in enumerate(layer):
            if(los_list[l][i] == 0):
                layer_comp.append([1, 1, 1, 1, 1])
            else:
                layer_comp.append(orbits[l][i].get_tasks())
        s_comp.append(layer_comp)
    return s_comp

def calc_doppler_shift(freq, vel, theta):
    return freq * vel * math.cos(theta) / (C/1000)

def calc_doppler_shift_on_x_list(freq, rel_vels, prop_angles) -> list:
    total = []
    for j, layer in enumerate(prop_angles):
        dop_layer = []

        for k, prop_angle in enumerate(layer):
            dop_layer.append(calc_doppler_shift(freq, rel_vels[j][k][0], prop_angle))

        total.append(dop_layer)
    return total

def calc_doppler_shift_on_y_list(freq, rel_vels, prop_angles) -> list:
    total = []
    for j, layer in enumerate(prop_angles):
        dop_layer = []
        
        for k, prop_angle in enumerate(layer):
            dop_layer.append(calc_doppler_shift(freq, rel_vels[j][k][1], prop_angle))

        total.append(dop_layer)
    return total

def get_distance_list(ac1: AirCraft, orbits) -> list:
    _los_orbits = []
    for orbit in orbits:  
        _los_orbit = []
        for sat in orbit:
            _los_orbits.append(get_distance(ac1, sat))

    return _los_orbits
