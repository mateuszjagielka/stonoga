import RPi.GPIO as GPIO
from time import *
from pygame import mixer
import os

# Files naming and modes
extention = '.wav'
directory = '/home/pi/sounds/'
filePrefix = ['ZS-', 'JK-', 'AD-', 'AM-']   # prefix per mode

# GPIOs
outPut = [2, 3, 17, 22, 10, 11, 5, 13]      # GPIO id according to keyboard lines: 1, 2, 3, 4, 5, 6, 7, 8
inPut = [4, 27, 9, 6]                       # GPIO id according to keyboard lines: 9, 10, 11, 12
modeSelectInPut = [24, 7, 16, 20]           # GPIO id according to cables no.: 3, 8, 7, 6 // modes: mode1, mode2, mode3, mode4
modeSelectOutPut = 26
# ledOutput = 15

# Keyboard matrix
MATRIX = [['P', 'O', 'N'], ['K', 'L', 'M'], ['S', 'R', 'Q'], ['H', 'I', 'J'], ['V', 'U', 'T'], ['E', 'F', 'G'],
          ['Z', 'Y', 'X', 'W'], ['A', 'B', 'C', 'D']]

# GPIOs init:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(len(outPut)):
    GPIO.setup(outPut[i], GPIO.OUT)

for i in range(len(inPut)):
    GPIO.setup(inPut[i], GPIO.IN)

for i in range(len(modeSelectInPut)):
    GPIO.setup(modeSelectInPut[i], GPIO.IN)

GPIO.setup(modeSelectOutPut, GPIO.OUT)

# GPIO.setup(ledOutput, GPIO.OUT)


# mixer init:
mixer.init()
soundFile = [[0 for x in range(4)] for y in range(8)]


# program main function

GPIO.output(modeSelectOutPut, GPIO.HIGH)

try:
    while True:

        # Select mode
        selectedMode = -1
        while True:
            if GPIO.input(modeSelectInPut[0]):
                selectedMode = 0
                sleep(1)
                for i in [1, 2, 3]:
                    if GPIO.input(modeSelectInPut[i]):
                        selectedMode = i

            if selectedMode != -1:
                break

            sleep(0.1)

        # Sound files assignment
        for i in range(len(outPut)):

            if i < 6:
                inputIterator = 3
            else:
                inputIterator = 4

            for j in range(inputIterator):
                soundFile[i][j] = mixer.Sound(directory + filePrefix[selectedMode] + MATRIX[i][j] + extention)

        # Play startup sound file
        startupFile = mixer.Sound(directory + filePrefix[selectedMode] + 'Startup' + extention)
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

                GPIO.output(outPut[i], GPIO.LOW)
            sleep(0.01)

            # Select mode
            testMode = -1
            if GPIO.input(modeSelectInPut[0]):
                testMode = 0
                for i in [1, 2, 3]:
                    if GPIO.input(modeSelectInPut[i]):
                        testMode = i

            if selectedMode != testMode:

                if mixer.get_busy():
                    while mixer.get_busy():
                        sleep(0.05)
                    sleep(0.2)
                endFile = mixer.Sound(directory + filePrefix[selectedMode] + 'End' + extention)
                endFile.play()
                os.system("echo Cześć! Tu Zbyszek Stonoga!")
                while mixer.get_busy():
                    sleep(0.1)
                sleep(0.2)
                # os.system("sudo poweroff")
                break

finally:
    GPIO.cleanup()
