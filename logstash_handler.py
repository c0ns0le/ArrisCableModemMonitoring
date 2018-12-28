import logging

import logstash

# TODO: Don't use a global variable here
# TODO: Allow the port number/elastic search address to be configurable via the command line parameter

global logstash_logger
logstash_logger = logging.getLogger('python-logstash-logger')
logstash_logger.setLevel(logging.DEBUG)
logstash_logger.addHandler(logstash.LogstashHandler('localhost', 5044, version=1))


def write_to_logstash(msg: str, level: int, timestamp: str) -> bool:
    logstash_logger.log(int(level) * 10, msg, extra={'desired_timestamp': str(timestamp)})

    return True
