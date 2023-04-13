import os 

try:
    import numpy as np
except:
    os.system("pip install numpy")

DATA_AMOUNT = 0
BAND_WIDTH = 50e9 # GHz
FREQUENCY = 340e9 # GHz
MAXIMUM_TIME = 0.1 # s
EARTH_CENTER_LOC = (0,0,0)

TRANSMISSION_POWER = 80 # dB

#### ABOUT ANTENNA
ANTENNA_DIAMETER                = 1.2 # m
ANTENNA_EFFICIENCY              = 0.9
RECEIVER_ANTENNA_EFFICIENCY     = 0.9
TRANSMITTER_ANTENNA_EFFICIENCY  = 0.9

TRANSMITTER_ANTENNA_GAIN        = 0.9
RECEIVER_ANTENNA_GAIN           = 0.9

#### NOISE CONSTANTS
ADDITIONAL_NOISE_RECEIVER = 0.1

#### SPACE CONDITION 
TEMPERATURE = 300 # K

#### SCIENTIFIC CONSTANTS
PI = np.pi
G = 6.6743e-11               # gravitational constant, m^3/(kg s^2)
M = 5.972e24                 # mass of Earth, kg
R = 6371000                  # radius of Earth, m
C = 300000000                # m/s
BOLTZMAN_CONSTANT = 1.38e-23 # J/K

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