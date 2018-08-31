#Slush system includes
import os
import sys

try:
    import spidev as spidev
    import RPi.GPIO as gpio
    import smbus2 as SMBus
except Exception as e:
    print (e.__doc__)
    print (e.message)

