#!/usr/bin/python3

# bus_access_DTH22

import time
import RPi.GPIO as GPIO
"""
DHT22 sends high bits first
DATA = 16 bit integer RH-data, 1 T-sign-bit (negative if 1), 15 bit integer T-data and 8 bit check sum
Checksum is adding the first 4 bytes and truncating to the last 8 bits

Raspberry PI 4 sends a start signal (pulse low for >1ms)
Raspberry PI 4 waits 20-40us for DHT22 response

DHT22 response is a LOW signal for 80us, then a HIGH for 80us with the data bits following

Data are coded as a LOW signal for >=50us, followed by high signal (70us for a 1, 26us to 28us for a 0)
"""

class Readsensor:
    def __init__(self, pin):
        self._pin = pin
        self._debug = False
        self._timmings:float = []
    
    def errorMsg(self, errorNo):
        if errorNo == -1:
            return("No response received back from DHT22")
        elif errorNo == -2:
            return("DTH22 and Raspberry Pi 4 are out of sync")
        elif errorNo == -3:
            return("Line stuck LOW")
        elif errorNo == -4:
            return("Underrun (no more bit)")
        elif errorNo == -5:
            return("Checksum error")
        elif errorNo == -6:
            return("No acknowledgement HIGH phase")
        else:
            return("No error")

    def setDebug(self, setit):
        self._debug = setit

    def _getbit(self):
        # DHT22 should have pulled the line LOW at this point, but let's check it anyway
        start = time.time()
        while GPIO.input(self._pin): # Wait for the line to go LOW
            if time.time() - start > 0.0001:
                return("S") # line is stuck HIGH before the bit. So maybe we missed the beginning of it
        # OK, the line is LOW. Wait for the bit now
        start = time.time()
        while not GPIO.input(self._pin): # Wait for the line to go HIGH (beginning of the bit)
            if time.time() - start > 0.0001:
                return("T") # Waiting for the line to go HIGH, but stuck LOW
        start = time.time() #OK, the line is HIGH. Let's measure the duration of the HIGH-phase
        while  GPIO.input(self._pin):
            if time.time() - start > 0.0001: # More than 100us. Line is stuck HIGH.
                return("U") # Line is stuck HIGH while waiting for the bit
        tim = time.time() - start
        self._timmings.append(tim)
        if tim > 0.000035: # 0 = 26-28us,  1=70us
            return("1")
        else:
            return("0")

    def _sendStartbit(self):
        GPIO.setup(self._pin, GPIO.OUT, initial = False)
        time.sleep(0.001) # Start pulse LOW for 1ms
        GPIO.output(self._pin,True) # Then pull line back HIGH
        GPIO.setup(self._pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def _waitResponse(self):
        # Response should come within 20-40 us from DTH22
        start = time.time() # Lockup protection
        while GPIO.input(self._pin): # Wait for line to be pulled LOW
            if time.time() - start > 0.0001: # If more than 100us, DHT22 does not respond!
                return(False)
        # we are now at the beginning of its response of 80 us
        return(True)

    def _waitAck(self):
        # Line must go HIGH after 80us
        time.sleep(0.000050)
        start = time.time() # Lockup protection
        while GPIO.input(self._pin): # Wait for the line to be pulled HIGH
            if time.time() - start > 0.0001: # DHT22 has not responded within 150 us
                return(False)
        # We are now ready for the data transmission to begin
        return(True)

    def _getData(self):
        st = ''
        for _ in range(40):
            st += self._getbit()
        return(st)

    def _validateData(self, data):
        if self._debug:
            print(data[0:8], data[8:16], data[16:24], data[24:32], data[32:40])
        for i in range(len(data)):
            if (data[i] < "0") or (data[i] > "1"):
                if data[i] == 'S':
                    return(-2) # Out of sync
                if data[i] == 'T':
                    return(-3) # Line stuck LOW
                if data[i] == 'U':
                    return(-4) # Underrun (Expected bit did not arrive)
        tl = 0
        for i in range(4):
            tl += int(data[i*8:i*8+8], 2)
        while tl > 255:
            tl -= 256
        if self._debug:
            print("Total added:",tl, "Chksum:",int(data[32:40], 2))
        if tl == int(data[32:40], 2): # Compare total to checksum
            return(0)
        return(-5) # Bad checksum

    def temp(self, retry = 3):
        # Set the line normal HIGH (pulled up)
        for tr in range(retry):
            self._timmings.clear()
            GPIO.setup(self._pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            time.sleep(1.5) # Wait for line to stabilize 
            self._sendStartbit()
            if not self._waitResponse():
                if tr == retry-1:
                    return(85, -1) # Error Ack LOW
                time.sleep(1.5)
                continue
            if not self._waitAck():
                if tr == retry-1:
                    return(85, -6) # Error Ack HIGH
                time.sleep(1.5)
                continue
            st = self._getData() # Get the 40 bits
            er = self._validateData(st)
            if er < 0:
                if tr == retry - 1:
                    return(85, er) # Timeout error
                time.sleep(0.5)
                continue
            hum = int(st[0:16], 2) / 10
            if st[16] == "1":
                temp = -int(st[17:32], 2) / 10
            else:
                temp = int(st[17:32], 2) / 10
            return(temp,hum)