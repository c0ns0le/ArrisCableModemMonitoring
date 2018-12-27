import logging

import logstash

global logstash_logger

logstash_logger = logging.getLogger('python-logstash-logger')
logstash_logger.setLevel(logging.DEBUG)
logstash_logger.addHandler(logstash.LogstashHandler('localhost', 5044, version=1))


def write_to_logstash(msg: str, level: str = "warning") -> bool:
    logstash_logger.warning("python-logstash: {0}".format(msg))

    return True
