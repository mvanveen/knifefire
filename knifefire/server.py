#!/usr/bin/env python

import logging
import time

import liblo
import netifaces
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.INFO)

MAX_ON_SECONDS = 2
NETWORK_DEVICE = 'eth0'
BROADCAST_IP = netifaces.ifaddresses(NETWORK_DEVICE)[2][0]['addr']
logging.info('broadcast ip: %s',  BROADCAST_IP)

RELAY_WIREUP = {
    '/knifefire/fire1': 16,
    '/knifefire/fire2': 16,
    '/knifefire/fire3': 16,
    '/knifefire/fire4': 16,
    '/knifefire/fire5': 16,
    '/knifefire/fire6': 16,
    '/knifefire/push7': 16,  #TODO (mvv): minor bug in layout, needs fixing
    '/knifefire/fire8': 16,
}


class KnifeFireServer(liblo.Server):
    def __init__(self, port):
        logging.info('knifefire server initialized')
        liblo.Server.__init__(self, port)
        self.setup_gpio()
        self.state = False
        self.RELAY_TIMINGS = {}
        self.RELAY_STATE = {}

    def setup_gpio(self):
        # BCM is actual GPIO pin numbers, not board pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._setup_pins()

    def _setup_pins(self):
        for relay, pin in RELAY_WIREUP.iteritems():
            assert isinstance(pin, int)
            logging.info('setting up pin %s for relay %s', pin, relay)
            GPIO.setup(pin, GPIO.OUT)

    def set_pin(self, relay_path, pin, value, *args):
        logging.info('setting pin %s to %s value', pin, value)

        if value:
            self.RELAY_TIMINGS[relay_path] = time.time()
            self.RELAY_STATE[relay_path] = 1
            GPIO.output(pin, GPIO.HIGH)
        elif value == 0:
            state_is_low = not self.RELAY_STATE.get(relay_path)
            if state_is_low:
                logging.warning('state should already be low on pin %s', pin)
            self.RELAY_STATE[relay_path] = 0
            GPIO.output(pin, GPIO.LOW)
        else:
            logging.error(
                "Not an acceptable value.  pin: %s, value: %s",
                pin,
                value
            )

    @liblo.make_method(None, None)
    def catch_all_msgs(self, path, args):
        logging.error('%s %s', path, args)

        pin = RELAY_WIREUP.get(path)
        if pin is None:
            logging.error('Pin wireup not detected: %s', path)
            return

        self.set_pin(path, pin, *args)
        return

    def serve(self):
        logging.info('knifefire server running')
        while True:
            # Drain all pending messages without blocking
            while self.recv(0):
                pass
            self.check_for_relay_on_too_long()

    def check_for_relay_on_too_long(self):
        now = time.time()
        for relay_path, trigger_time in self.RELAY_TIMINGS.iteritems():
            pin = RELAY_WIREUP.get(relay_path)
            state_is_high = self.RELAY_STATE.get(relay_path)
            if state_is_high and (now > (trigger_time + MAX_ON_SECONDS)):
                logging.info('Timeout detected, shutting off pin %s', pin)
                self.set_pin(relay_path, pin, GPIO.LOW)


if __name__ == '__main__':
    try:
       kfs = KnifeFireServer(8000)
       kfs.serve()
    finally:
       import RPi.GPIO as GPIO
       GPIO.cleanup()
