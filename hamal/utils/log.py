# -*- coding:utf-8 -*-
__author__ = 'luolin'

import logging
import os
import logging.handlers
from auto_openstack.util import singleton

class Log(object):
    __metaclass__ = singleton.singleton

    def __init__(self):
        self._init_env()

    def _init_env(self):
        LOG_FILE = '/var/log/automos/automos.log'
        try:
            exist = os.path.exists('/var/log/automos')
            if False == exist:
                os.makedirs('/var/log/automos')
        except OSError, why:
            raise Exception("/var/log/automos path operate error! %s" % why)

        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
        fmt = '%(asctime)s %(filename)s:%(lineno)s %(levelname)-8s [-] %(message)s'

        formatter = logging.Formatter(fmt)   # 实例化formatterog
        handler.setFormatter(formatter)      # 为handler添加formatter

        self.logger = logging.getLogger('automos')    # 获取名为tst的logger
        self.logger.addHandler(handler)           # 为logger添加handler
        self.logger.setLevel(logging.DEBUG)

    def log_info(self, msg):
        self.logger.info(msg)

    def log_debug(self, msg):
        self.logger.debug(msg)

    def log_error(self, msg):
        self.logger.error(msg)

    def log_warn(self, msg):
        self.logger.warn(msg)

    def log_critical(self, msg):
        self.logger.critical(msg)

def LOG_INFO(msg):
    Log().log_info(msg)

def LOG_DEBUG(msg):
    Log().log_debug(msg)

def LOG_ERROR(msg):
    Log().log_error(msg)

def LOG_WARN(msg):
    Log().log_warn(msg)

def LOG_CRITICAL(msg):
    Log().log_critical(msg)
