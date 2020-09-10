#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import readtempDTH11

def main():
    GPIO.setmode(GPIO.BCM)
    sigPort = 18
    try:
        readtemp = readtempDTH11.Readtemp(sigPort)
        time.sleep(1)
        while True:
            temp, hum = readtemp.temp()
            if hum < 0:
                print(readtemp.errorMsg(hum))
            else:
                print("Temp: "+str(temp)+"°C  Humidity:"+str(hum)+"%")
            time.sleep(2) # datasheet specifies no less than 2 seconds between calls
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        print("Cleaning up")
        GPIO.cleanup()

if __name__ == '__main__':
    main()