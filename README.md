DHT11

DTH11 humidity sensor tiny app based on software for DHT22 from github!

Just copy both files (humidity.py and readtempDTH11.py into the same directory and execute humidity.py in Python. The Readtemp() argument is the GPIO number in use.

Not sure if this is done by the book but it seems to be working.

It would be good to disable the pi interrupt during the read operation from DTH11 because the timing seems to be quite sensitive.

The temp() function could have an argument:retry=n

By default, it is set to 3