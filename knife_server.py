#!/usr/bin/env python

import time

import liblo
import RPi.GPIO as GPIO

BROADCAST_IP = '10.0.0.4'


class KnifeFireServer(liblo.ServerThread):

    def __init__(self, port):
        liblo.ServerThread.__init__(self, port)
        self.setup_gpio()
        self.state = False

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)
        # TODO: set up pins

    @liblo.make_method(None, None)
    def catch_all_msgs(self, path, args):
        print path
        #if path == '/water/mist':
        #   GPIO.output(16, self.state and GPIO.HIGH or GPIO.LOW)
        #   self.state = not self.state 
        #print args
        #return

    def serve(self):
        while True:
            pass

if __name__ == '__main__':
    kfs = KnifeFireServer(8000)
    kfs.start()
    kfs.serve()
