'''
Loads up each users config and creates the service watchers
'''
import yaml

def load_config(filename):
    '''Loads config file,
    format is in yaml

    and looks like:

    services:
        - name: openvpn
          input: 10
          output: 2
        - name: samba
          input: 10
          output: 2
    '''
    with open(filename) as f:
        config = yaml.load(f)

    assert 'services' in config, "no services in config"

    services = []
    for service in config['services']:
        assert 'name' in service, 'Missing code for one service '
        assert 'input' in service, 'Missing input pin for {}'.format(service['name'])
        assert 'output' in service, 'Missing output pin for {}'.format(service['name'])

    return config


if __name__ == '__main__':
    print(load_config('./sample.yaml'))
