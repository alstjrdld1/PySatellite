import os 

try:
    import numpy as np
except:
    os.system("pip install numpy")

DATA_AMOUNT = 0
BAND_WIDTH = 200
FREQUENCY = 200 # 
MAXIMUM_TIME = 0.1 # s
EARTH_CENTER_LOC = (0,0,0)
TRANSMISSION_POWER = 3 # dB

PI = np.pi
G = 6.6743e-11  # gravitational constant, m^3/(kg s^2)
M = 5.972e24    # mass of Earth, kg
R = 6371000     # radius of Earth, m
C = 300000000   # m/s

##### FOR DRL 
BATCH_SIZE = 128
LR = 0.01
GAMMA = 0.90
EPISILO = 0.9
MEMORY_CAPACITY = 2000
Q_NETWORK_ITERATION = 100

NUM_ACTIONS = 5
NUM_STATES = 5
HIDDEN_SIZE = 64