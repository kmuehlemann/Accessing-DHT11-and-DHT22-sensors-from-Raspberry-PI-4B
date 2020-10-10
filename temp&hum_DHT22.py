#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import bus_access_DHT22

def main():
    GPIO.setmode(GPIO.BCM)
    sigPort = 18
    try:
        readsensor = bus_access_DHT22.Readsensor(sigPort)
        time.sleep(1)
        while True:
            temp, hum = readsensor.temp()
            if hum < 0: # A negative humidity value is code for an error
                print(readsensor.errorMsg(hum))
            else:
                print("Temp: "+str(temp)+"°C  |  Rel. Humidity: "+str(hum)+"%")
            time.sleep(2) # datasheet specifies no less than 2 seconds between calls
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
        print("Cleaning up")
        GPIO.cleanup()

if __name__ == '__main__':
    main()