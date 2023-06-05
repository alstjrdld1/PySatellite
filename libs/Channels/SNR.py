from libs.Constants import *
from libs.Channels.Loss import *

import math

def get_snr_fspl(distance,
                 frequency          = FREQUENCY, 
                 transmitter_power  = TRANSMISSION_POWER, 
                 transmitter_gain   = TRANSMITTER_ANTENNA_GAIN, 
                 receiver_gain      = RECEIVER_ANTENNA_GAIN, 
                 noise_figure       = ADDITIONAL_NOISE_RECEIVER):
    
    # Convert input to linear scale
    transmitter_power_lin = 10 ** (transmitter_power / 10)
    transmitter_gain_lin = 10 ** (transmitter_gain / 10)
    receiver_gain_lin = 10 ** (receiver_gain / 10)
    noise_figure_lin = 10 ** (noise_figure / 10)

    # Calculate wavelength (m)
    wavelength = C / frequency

    # Calculate free space path loss (FSPL)
    fspl = FSPL(distance, wavelength)

    # Calculate received power (linear scale)
    received_power_lin = transmitter_power_lin * transmitter_gain_lin * receiver_gain_lin / (1+fspl)

    # Calculate noise power (linear scale)
    noise_power_lin = BOLTZMAN_CONSTANT * TEMPERATURE * noise_figure_lin * frequency

    # Calculate SNR (linear scale)
    snr_lin = received_power_lin / noise_power_lin

    # Convert SNR to dB scale
    snr_db = 10 * math.log10(snr_lin)

    return snr_db

def get_snr_fspl_doppler(distance,
                         frequency          = FREQUENCY, 
                         transmitter_power  = TRANSMISSION_POWER, 
                         transmitter_gain   = TRANSMITTER_ANTENNA_GAIN, 
                         receiver_gain      = RECEIVER_ANTENNA_GAIN, 
                         noise_figure       = ADDITIONAL_NOISE_RECEIVER,
                         velocity           = 0,
                         angle              = 0):
    
    # Convert input to linear scale
    transmitter_power_lin = 10 ** (transmitter_power / 10)
    transmitter_gain_lin = 10 ** (transmitter_gain / 10)
    receiver_gain_lin = 10 ** (receiver_gain / 10)
    noise_figure_lin = 10 ** (noise_figure / 10)

    # Calculate free space path loss (FSPL)
    fspl = FSPL_doppler(distance, frequency, velocity, angle) # dB
    if(fspl == 0):
        fspl = 1

    # Atmospheric Attenuation 
    aa = atmospheric_attenuation(frequency) * distance # dB

    l_tot = fspl + aa
    # print("L tot : ", l_tot)

    # Calculate received power (linear scale)
    # received_power_lin = transmitter_power_lin * transmitter_gain_lin * receiver_gain_lin / (1+fspl)
    received_power_lin = transmitter_power_lin * transmitter_gain_lin * receiver_gain_lin / l_tot

    # Calculate noise power (linear scale)
    noise_power_lin = BOLTZMAN_CONSTANT * TEMPERATURE * noise_figure_lin * frequency

    # Calculate SNR (linear scale)
    snr_lin = received_power_lin / noise_power_lin
    # return snr_lin

    # Convert SNR to dB scale
    try:
        snr_db = 10 * math.log10(snr_lin)
        # print("SNR : ", snr_db)
        return snr_db
    except:
        print("SNR LINEAR SCALE : ", snr_lin)
        raise


def get_snr_consider_antenna_diameter(distance, velocity, velocity_angle):
    _freq = FREQUENCY * velocity  * abs(math.cos(velocity_angle) / C)
    _Pr = (TRANSMISSION_POWER * (ANTENNA_EFFICIENCY**2) * (PI**2) * (ANTENNA_DIAMETER**4) * (_freq**2)) / (16 * (C **2) * (distance**2))
    _snr = _Pr / (ADDITIONAL_NOISE_RECEIVER*BOLTZMAN_CONSTANT*TEMPERATURE*BAND_WIDTH)
    return _snr