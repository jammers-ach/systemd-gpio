'''
Classes for watching a systemd service
'''
import subprocess
import logging
import time

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)


class ServiceWatcher():
    '''
    Wathes a systemd service, based on a switch port and an led port.
    When the switch changes state the service is started/stopped

    the LED will be solid wen the serivce stops
    it will flash slowly when it's starting up
    it will flash quickly when it's shutting down

    when the class is instaciated it will check the switch status
    and if it differs from the actual status it will change it
    '''
    flash_freq = 0.1 # interval in seconds of flashing while service is canging
    service_timeout = 15 # seconds while we're waiting for the service status to change

    def __init__(self, procname, sw_port, led_port):
        self.procname = procname
        self.sw_port = sw_port
        self.led_port = led_port

        GPIO.setup(sw_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(led_port, GPIO.OUT, initial=GPIO.LOW)

        self.update_service()

        GPIO.add_event_detect(sw_port,
                              GPIO.BOTH,
                              callback=self.switch_callback,
                              bouncetime=200)


    @property
    def _system_status(self):
        '''Gets the status of the service:
            the same as the output of system service
         '''
        output = subprocess.run(['service', self.procname, 'status'],
                                stdout=subprocess.PIPE).stdout.decode('utf-8')
        for line in output.split('\n'):
            if line.strip().startswith('Active: '):
                status = line.split()[1]
                return status
        raise Exception('Could not get status for {}'.format(self.procname))


    def _stop_service(self):
        logger.info("Stopping {}".format(self.procname))
        subprocess.Popen(['service', self.procname, 'stop'])
        self._watch_loop('inactive')

    def _start_service(self):
        logger.info("Starting {}".format(self.procname))
        subprocess.Popen(['service', self.procname, 'start'])
        self._watch_loop('active')


    def switch_callback(self, port):
        '''
        callback for swtiches
        '''
        logger.debug("SWITCH")
        if port == self.sw_port:
            self.update_service()
        else:
            logger.error("Got interupt on {}, but {} is on {}".format(port, self.procname, self.sw_port))

    def update_service(self):
        '''Sets the service status to match the switch status'''
        service_status = self._system_status
        switch_status = self.switch_status
        logger.debug("Switch: {}, Service: {}".format(switch_status, service_status))
        if switch_status and service_status == 'inactive':
            self._start_service()
        elif not switch_status and service_status != 'inactive':
            self._stop_service()


    def _watch_loop(self, desired_state):
        '''Loops '''
        count = 0
        led_state = True
        self.update_led(desired_state == 'active')
        while self._system_status != desired_state:
            led_state = not led_state
            time.sleep(self.flash_freq)
            count += 1
            if count > (self.service_timeout/self.flash_freq):
                raise Exception("timed out waiting for {}".format(self.procname))
        self.update_led(desired_state == 'active')

    def update_led(self, state):
        '''sets the LEDs state: true for on false for off
        '''
        logger.debug('LED: {} '.format((state)))
        GPIO.output(self.led_port, 1 if state else 0)

    @property
    def switch_status(self):
        '''returns true if switch is on (i.e. the service
        should be on)
        '''
        return GPIO.input(self.sw_port) == 1

# All GPIO related work is based on
# http://raspberry.io/projects/view/reading-and-writing-from-gpio-ports-from-python/



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    GPIO.setmode(GPIO.BOARD)

    s = ServiceWatcher('bluetooth', 11, 12)

    try:
        while True:
            time.sleep(5)
            print(s._system_status)
    finally:
        GPIO.cleanup()

