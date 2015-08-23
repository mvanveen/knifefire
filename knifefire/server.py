#!/usr/bin/env python

import logging
import time

import liblo
import netifaces
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.INFO)

NETWORK_DEVICE = 'eth0'
BROADCAST_IP = netifaces.ifaddresses(NETWORK_DEVICE)[2][0]['addr']
logging.info('broadcast ip: %s',  BROADCAST_IP)

RELAY_WIREUP = {
    '/knifefire/knife1': 16
}


class KnifeFireServer(liblo.Server):
    def __init__(self, port):
        logging.info('knifefire server initialized')
        liblo.Server.__init__(self, port)
        self.setup_gpio()
        self.state = False

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

    @liblo.make_method(None, None)
    def catch_all_msgs(self, path, args):
        logging.error(path, args)
        #if path == '/water/mist':
        #   GPIO.output(16, self.state and GPIO.HIGH or GPIO.LOW)
        #   self.state = not self.state 
        #print args
        #return

    def serve(self):
        logging.info('knifefire server running')
        while True:
            # Drain all pending messages without blocking
            while self.recv(0):
                pass


if __name__ == '__main__':
#
#    try:
#        server = AMCPServer(port=8000, client_ip=BROADCAST_IP, client_port=9000)
#    except liblo.ServerError, err:
#        print str(err)
#        sys.exit()
#
#    if platform.system() == "Darwin":
#        service = None
#    else:
#        # Avahi announce so it's findable on the controller by name
#        from avahi_announce import ZeroconfService
#        service = ZeroconfService(
#            name="AMCP TouchOSC Server", port=8000, stype="_osc._udp")
#        service.publish()
#
#    # Main thread runs both our LED effects and our OSC server,
#    # draining all queued OSC events between frames. Runs until killed.

    try:
       kfs = KnifeFireServer(8000)
       kfs.serve()
    finally:
       import RPI.GPIO as GPIO
       GPIO.cleanup()
