import RPi.GPIO as GPIO
from time import *
from pygame import mixer
import os

# Settings begins here

# GPIOs
outPut = [2, 3, 17, 22, 10, 11, 5, 13]   # GPIO id according to keyboard lines: 1, 2, 3, 4, 5, 6, 7, 8
inPut = [4, 27, 9, 6]                    # GPIO id according to keyboard lines: 9, 10, 11, 12
modeInPut = [24, 20, 16, 7]              # GPIO id according to cables no.: 3, 8, 7, 6 // modes: mode0, mode1, mode2, mode3
# ledOutput = 15


# File sets names
extention = '.wav'
directory = '/home/pi/sounds/'
modesName = ['ZS-', '', '', '']

k = 0


# Constants
MATRIX = [['P', 'O', 'N'], ['K', 'L', 'M'], ['S', 'R', 'Q'], ['H', 'I', 'J'], ['V', 'U', 'T'], ['E', 'F', 'G'],
          ['Z', 'Y', 'X', 'W'], ['A', 'B', 'C', 'D']]




# GPIOs initial settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(len(outPut)):
    GPIO.setup(outPut[i], GPIO.OUT)

for i in range(len(inPut)):
    GPIO.setup(inPut[i], GPIO.IN)

# GPIO.setup(26, GPIO.IN)

# GPIO.setup(ledOutput, GPIO.OUT)


# mixer init:
mixer.init()
soundFile = [[0 for x in range(4)] for y in range(8)]

# sound files init:
for i in range(len(outPut)):

    if i < 6:
        inputIterator = 3
    else:
        inputIterator = 4

    for j in range(inputIterator):
        soundFile[i][j] = mixer.Sound(directory + modesName[k] + MATRIX[i][j] + extention)


# program main function

for i in range(len(outPut)):
    GPIO.output(outPut[i], GPIO.LOW)

try:

    startupFile = mixer.Sound(directory + modesName[k] + 'Startup' + extention)
    startupFile.play()
    del startupFile

    while True:

        for i in range(len(outPut)):

            GPIO.output(outPut[i], GPIO.HIGH)

            if i < 6:
                inputIterator = 3
            else:
                inputIterator = 4

            for j in range(inputIterator):

                if GPIO.input(inPut[j]):

                    mixer.stop()

                    soundFile[i][j].play()

                # if mixer.get_busy():
                #     GPIO.output(ledOutput, GPIO.HIGH)
                # else:
                #     GPIO.output(ledOutput, GPIO.LOW)

                while GPIO.input(inPut[j]):
                    sleep(0.1)

                sleep(0.01)

            GPIO.output(outPut[i], GPIO.LOW)

            # if GPIO.input(26):
            #     mixer.stop()
            #     endFile = mixer.Sound(directory + modesName[k] + 'End' + extention)
            #     endFile.play()
            #     os.system("echo Cześć! Tu Zbyszek Stonoga!")
            #     while GPIO.input(26):
            #         sleep(0.1)
            #     while mixer.get_busy():
            #         sleep(0.1)
            #     # os.system("sudo poweroff")

        sleep(0.1)

finally:
    GPIO.cleanup()
