# How to use 

## To calculate channel loss 
    # caculate distance between two nodes. 
    # And put wave_length in your condition

    fspl = FSPL(distance, wave_length)

## To calculate snr (Signal Noise Ratio)
    # caculate distance between two nodes. 

    _snr = get_snr_fspl(distance=_dist)


## To calculate Achievable rate (Datarate)
    # caculate distance between two nodes. 

    _snr = get_snr_fspl(distance=_dist)
    _cp = shannon_hartley(_snr)
    

        