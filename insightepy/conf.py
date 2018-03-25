import configparser
import logging
import os
import sys


class __DefaultConf(object):
    confs = dict(
        log=dict(
            level='INFO',
            log_file='',
        ),
        dependencies=dict(
            locations='',
        ),
        server=dict(
            host='176.31.255.107',
            port='9500',
            route_prefix='',
        ),
        test=dict(
            client_id='',
            client_secret='',
            auth_token='',
        )
    )

    def get(self, section, param):
        return self.confs[section][param]


INI_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../conf/conf.ini')

if os.path.exists(INI_FILE):
    config = configparser.ConfigParser()
    config.read(INI_FILE)
else:
    config = __DefaultConf()


def get_config(section, param):
    return config.get(section, param)


# logger
fmt = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL = config.get('log', 'level')
log_file = config.get('log', 'log_file')
if log_file.strip() == '':
    logging.basicConfig(format=fmt, datefmt=datefmt, level=LOG_LEVEL)
else:
    logging.basicConfig(format=fmt, datefmt=datefmt, level=LOG_LEVEL, filename=log_file)

logger = logging.getLogger('Conf')

# importing dependencies
dependency_locations = filter(
    lambda d: d != '',
    map(
        lambda d: d.strip(),
        config.get('dependencies', 'locations').split(',')
    )
)
for location in dependency_locations:
    logger.debug('Injecting Dependency: "{}"'.format(location))
    sys.path.append(location)
