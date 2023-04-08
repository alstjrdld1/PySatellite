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






