from libs.Constants import *
import math 

def shannon_hartley(snr,
                    bandwidth = BAND_WIDTH):
    """
    Calculate the maximum data rate using the Shannon-Hartley theorem.

    Args:
    - channel_bandwidth (float): The channel bandwidth in Hz
    - snr_linear (float): The signal-to-noise ratio (SNR) in db

    Returns:
    - data_rate (float): The maximum data rate in bits per second (bps)
    """
    snr_linear = 10**(snr / 10)
    return bandwidth * math.log2(1 + snr_linear)