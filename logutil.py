# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:48:35 2017

@author: vijayp
"""
import logging
import logging.handlers

class Logutil:
    def set_up_logging(logfilepath):
        logFolder = r'C:\Users\vijayp\Documents\Python Scripts\finigence\log\\'
        # File handler for /var/log/some.log
        serverlog = logging.FileHandler(logFolder+logfilepath)
        serverlog.setLevel(logging.DEBUG)
        serverlog.setFormatter(logging.Formatter( '%(asctime)s %(pathname)s [%(process)d]: %(levelname)s %(message)s'))
        # Syslog handler
        syslog = logging.handlers.SysLogHandler()
        syslog.setLevel(logging.WARNING)
        syslog.setFormatter(logging.Formatter( '%(pathname)s [%(process)d]: %(levelname)s %(message)s'))
        # Combined logger used elsewhere in the script
        logger = logging.getLogger('finigence')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(serverlog)
        logger.addHandler(syslog)
        return logger