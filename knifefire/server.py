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
#
#    try:
#        server.mainLoop()
#    except KeyboardInterrupt:
#        # Cleanup
#        if service:
#            service.unpublish()
#        if OnPi():
#            import RPi.GPIO as GPIO
#            GPIO.cleanup()
#
#    finally:
#        logger.info('action="server_shutdown"')
#
#        # Cleanup
#        if service:
#            service.unpublish()
#        if OnPi():
#            import RPi.GPIO as GPIO
#            GPIO.cleanup()

    kfs = KnifeFireServer(8000)
    kfs.start()
    kfs.serve()
