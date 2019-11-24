'''
Classes for watching a systemd service
'''
import subprocess
import logging
import time

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
    flash_freq = 0.1

    def __init__(self, procname, sw_port, led_port):
        self.procname = procname
        self.sw_port = sw_port
        self.led_port = led_port
        self.update_service()

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
                logger.debug(line)
                return status
        raise Exception('Could not get status for {}'.format(self.procname))


    def _stop_service(self):
        output = subprocess.run(['service', self.procname, 'stop'],
                       stdout=subprocess.PIPE).stdout.decode('utf-8')
        logger.debug(output)

    def _start_service(self):
        output = subprocess.run(['service', self.procname, 'start'],
                       stdout=subprocess.PIPE).stdout.decode('utf-8')
        logger.debug(output)

    def update_service(self):
        if self.switch_status and self._system_status == 'inactive':
            self._start_service()
        elif not self.switch_status and self._system_status != 'inactive':
            self._stop_service()


    def _watch_loop(self, desired_state):
        '''Loops '''
        led_state = True
        while self._system_status != desired_state:
            self.update_led(led_state)
            led_state = ! led_state
            time.sleep(self.flash_freq)


    def update_led(self, state):
        '''sets the LEDs state: true for on false for off
        '''
        print('LED: ', state)

    @property
    def switch_status(self):
        '''returns true if switch is on (i.e. the service
        should be on)
        '''
        return True

# All GPIO related work is based on
# http://raspberry.io/projects/view/reading-and-writing-from-gpio-ports-from-python/



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    s = ServiceWatcher('openvpn', 20, 20)

    print(s._system_status)
