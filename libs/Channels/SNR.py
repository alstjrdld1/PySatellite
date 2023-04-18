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