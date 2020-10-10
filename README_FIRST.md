I have struggled with Adafruit and their impressive BLINKA-software package, but could not get it to work. Actually, I am not interested in all the bells and whistles,
but just wanted to get my DHT11 and DHT22 sensors to work. And, most of all, I wanted to understand the basic evaluation program. In short, I was about to give up when I came across the link:

https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/27

Github user guytas wrote: "...I got fed up dealing with stack of problems just to read this device. I wrote a simple python program that sends the start signal via
the GPIO output, and then reads the 40 bits from the dth22, and get the result in humidity and temperature. It is a very simple process that uses only the gpio and
time libraries. What else should we really need?"

He published his work under guytas/dht22 from where I took it and adapted it for my purposes. Guytas work was an eye-opener to me (since I am a bloody beginner).
Nevertheless, I was able to make the program more stable and to adapt it to my needs. Here, I would like to share my work.
