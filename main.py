from config import load_config
import systemwatcher
import logging

logger = logging.getLogger(__name__)

def _main(filename):
    config = load_config(filename)
    watchers = []
    for s in config['services']:
        sw = systemwatcher.ServiceWatcher(s['name'], s['input'], s['output'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    _main('./sample.yaml')
