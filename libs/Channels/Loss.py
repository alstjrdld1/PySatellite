from libs.Constants import *
import math

def FSPL(distance, wave_length):
    return (4 * PI * distance / wave_length) ** 2

def FSPL_doppler(distance, frequency, relative_velocity, angle):
    try:
        shifted = (frequency * relative_velocity * math.cos(angle)) / (C / 1000)
        return ((4 * PI * distance * shifted) / (C / 1000))**2
    except:
        print("Frequency : ", frequency, "Relative Velocity : ", relative_velocity, "Angle : ", angle)
        raise

def atmospheric_attenuation(frequency = 2.4e9, temperature = 25.0, pressure = 1013.25, humidity = 50.0, elevation_angle = 0.0):
    """
    Calculate atmospheric attenuation using ITU-R P.676-11 model.
    
    Arguments:
    - frequency: Frequency of the RF signal in Hz.
    - temperature: Temperature in degrees Celsius.
    - pressure: Atmospheric pressure in hPa.
    - humidity: Relative humidity in percentage (0-100).
    
    Returns:
    - Attenuation in dB/km.
    """
    # Convert temperature to Kelvin
    temperature += 273.15
    temperature = TEMPERATURE
    
    # Convert pressure to Pascal
    pressure *= 100
    
    # Calculate saturation vapor pressure
    e = 6.1121 * math.exp((18.678 - (temperature / 234.5)) * (temperature / (257.14 + temperature)))
    
    # Calculate actual vapor pressure
    e_actual = (humidity / 100) * e
    
    # Calculate water vapor density
    rho_v = (e_actual * 216.7) / (temperature + 273.3)
    
    # Calculate attenuation due to dry air
    p = 1.0  # Reference pressure in hPa
    t = 288.0  # Reference temperature in Kelvin
    alpha_dry = 0.1820 * (pressure / p) * (t / temperature)**(1.5) * (frequency / 1e9)**2
    
    # Calculate attenuation due to water vapor
    alpha_wet = (3.01 * rho_v * (frequency / 1e9)**2) / (temperature + 273.0)
    
    # Calculate total attenuation
    attenuation = (alpha_dry + alpha_wet)
    
    return attenuation
