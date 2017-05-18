import logging

import sys


class LogFilter(logging.Filter):
    '''Filters (lets through) all messages with level < LEVEL'''

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno < self.level  # "<" instead of "<=": since logger.setLevel is inclusive, this should be exclusive


MIN_LEVEL = logging.DEBUG
stdout_hdlr = logging.StreamHandler(sys.stdout)
stderr_hdlr = logging.StreamHandler(sys.stderr)
log_filter = LogFilter(logging.WARNING)
stdout_hdlr.addFilter(log_filter)
stdout_hdlr.setLevel(MIN_LEVEL)
stderr_hdlr.setLevel(max(MIN_LEVEL, logging.WARNING))

formatter = logging.Formatter('%(message)s')
stdout_hdlr.setFormatter(formatter)
stderr_hdlr.setFormatter(formatter)

log = logging.getLogger()
log.addHandler(stdout_hdlr)
log.addHandler(stderr_hdlr)
log.setLevel(logging.DEBUG)
