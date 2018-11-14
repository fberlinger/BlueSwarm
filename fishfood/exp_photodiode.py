"""Using the photodiode to start multiple robots simultaneously

Attributes:
    caudal: Fin object for caudal fin
    depth_sensor: DepthSensor object
    dorsal: Fin object for dorsal fin
    leds: LED object
    pecto_l: Fin object for pectoral left fin
    pecto_r: Fin object for pectoral right fin
    photodiode: Photodiode object
    vision: Vision object
"""
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

import os
import csv
import time
import threading
import numpy as np
from math import *
from picamera import PiCamera

from lib_utils import *
from lib_fin import Fin
from lib_leds import LEDS
from lib_vision import Vision
from lib_depthsensor import DepthSensor
from lib_photodiode import Photodiode
from lib_ema import EMA

os.makedirs('./{}/'.format(U_FILENAME))


def initialize():
    """Initializes all threads which are running fins
    """
    threading.Thread(target=caudal.run).start()
    threading.Thread(target=dorsal.run).start()
    threading.Thread(target=pecto_l.run).start()
    threading.Thread(target=pecto_r.run).start()

    leds.on()
    time.sleep(1)
    leds.off()
    time.sleep(1)

def terminate():
    """Terminates all threads which are running fins
    """
    caudal.terminate()
    dorsal.terminate()
    pecto_l.terminate()
    pecto_r.terminate()

    leds.on()
    time.sleep(1)
    leds.off()

    GPIO.cleanup()

def idle():
    """Waiting for starting signal
    """
    thresh_photodiode = 50 # lights off: 2, lights on: 400 -> better range!

    while photodiode.brightness > thresh_photodiode:
        photodiode.update()
        print('idle {}'.format(photodiode.brightness))

def main(run_time=60):
    """Run fish
    
    Args:
        run_time (int, optional): Experiment time, [s]
    """
    t_start = time.time()

    while time.time() - t_start < run_time:
        photodiode.update()
        print('active {}'.format(photodiode.brightness))

caudal = Fin(U_FIN_C1, U_FIN_C2, 5) # freq, [Hz]
dorsal = Fin(U_FIN_D1, U_FIN_D2, 6) # freq, [Hz]
pecto_r = Fin(U_FIN_PR1, U_FIN_PR2, 8) # freq, [Hz]
pecto_l = Fin(U_FIN_PL1, U_FIN_PL2, 8) # freq, [Hz]
leds = LEDS()
vision = Vision()
depth_sensor = DepthSensor()
photodiode = Photodiode()

initialize()
idle()
leds.on()
main(60) # run time
leds.off()
terminate()
