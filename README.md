DHT11-Software and DHT22-Software
---------------------------------

The DTH11 and DHT22 humidity sensor tiny apps are both based on software for DHT22 from github!

Just copy either pair of files (temp&hum_DHT11.py and sensor_access_DTH11.py or temp&hum_DHT22.py
and sensor_access_DHT22.py, respectively, into the same directory). Then execute temp&hum_DHT11 or
temp&hum_DHT22 in Python. The Readsensor() argument is the GPIO number in use.

Of course, bus_access_DHT11.py and bus_access_DHT22.py could be combined into a single software. In
this case, a parameter for the type of the sensor (DHT11 or DHT22) would have passed to it. The
existing separate bus_access_DHTxx.py-versions take care of the subtle differences between the
sensors:
(1) The start LOW pulse is >18ms for DHT11 and >1ms for DHT22, respectively.
(2) The data readout format of DHT11 consists of integer and decimal values for relative humidity and
temperature [°C] whereas the readout format of DHT22 consists of a 16-bit binary value of 10x the
relative humidity and a 15-bit binary value of 10x the temperatur [°C] with the MSB acting as the
sign bit (1 for negative temperatures).

The temp() function could has an argument: retry=n. By default, it is set to 3.