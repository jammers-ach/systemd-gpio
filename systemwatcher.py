'''
Classes for watching a systemd service
'''




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

    def __init__(self, procname, sw_port, led_port):
        self.procname = procname
        self.sw_port = sw_port
        self.led_port = led_port


    @property
    def system_status(self):
        '''Gets the status of the service:
            active
            stopped
            starting
         '''
        pass

    @property
    def switch_status(self):
        '''returns true if switch is on (i.e. the service
        should be on)
        '''
        pass


    def stop_service(self):
        pass

    def start_service(self):
        pass

    def update_led(self, state):
        '''sets the LEDs state, one of:
            off, on, quick_flash, slow_flash
        '''
        pass

    def update_service(self):
        if self.switch_status and self.system_status == 'stopped':
            self.start_service()
        elif not self.switch_status and self.system_status != 'stopped':
            self.stop_service()



# All GPIO related work is based on
# http://raspberry.io/projects/view/reading-and-writing-from-gpio-ports-from-python/

