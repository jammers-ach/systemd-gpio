from config import load_config
import systemwatcher
import logging
import RPi.GPIO as GPIO
import time

logger = logging.getLogger(__name__)

def _main(filename):
    config = load_config(filename)
    GPIO.setmode(GPIO.BOARD)

    watchers = []
    for s in config['services']:
        sw = systemwatcher.ServiceWatcher(s['name'], s['input'], s['output'])

    try:
        while True:
            time.sleep(60)
            print('sleeping')
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    _main('./sample.yaml')
