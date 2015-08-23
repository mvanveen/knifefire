#!/usr/bin/python

import time
import RPi.GPIO as GPIO

"""
All this is supposed to do is flip the relay open and closed

The SainSmart relays are "active low", which means a pin must
be pulled low for the normally open terminals of the relay to
be closed, i.e. the relay to be triggered.  This is a safety
"feature"

Additionally, they are 5V relays, which means they want 5 V to
activate mechanically.  GPIO on the Raspberry Pi is 3.3V.  It
is important to connect the 3.3V from the RasPi board to the
VCC of the GPIO signal pins on the relay board - this is what
is understood as "high".  Otherwise, a small blinking red light
will fire, but the relay won't actually close.

"""

def main():
    try:
        GPIO.setmode(GPIO.BCM) # BCM is actual GPIO pin numbers, not board pins
        GPIO.setwarnings(False)
        GPIO.setup(4, GPIO.OUT)
        blinks = 0
        while True:
            blinks += 1
            print "lights on %d" % blinks
            GPIO.output(4, 0)
            time.sleep(0.5)
            print "lights off %d" % blinks
            GPIO.output(4, 1)
            time.sleep(0.5)
            if blinks == 100:
                break

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
