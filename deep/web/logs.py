"""
  @file    logs.py
  @brief   all log systems
  @details Copyright (c)
  @author  Nikolay Vovk
  @since   $Id: $
"""

import os
import time
from enum import Enum
import logging.handlers as handlers
import logging

import web.config as config
cfg = config.read()

log_max_file_size = cfg.get('log_max_file_size', 0)
log_max_files_count = cfg.get('log_max_files_count', 0)
log_when = cfg.get('log_when', 'd')
log_interval = cfg.get('log_interval', 1)

log_file_debug = cfg.get('log_file_debug',  'logs/debug.log')
log_file_debug_level = cfg.get('log_file_debug_level',  logging.DEBUG)
log_file_database = cfg.get('log_file_database', 'logs/database.log')
log_file_errors = cfg.get('log_file_errors', 'logs/errors.log')
log_file_perf = cfg.get('log_file_perf', 'logs/performance.log')

"""
directory = 'logs'
if not os.path.exists(directory):
    os.makedirs(directory)
Level   Numeric value
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""
DBG = logging.getLogger('debug_logger')

class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):

    def __init__(self, filename, maxBytes=0, when='midnight', interval=1,
                 backupCount=0, encoding=None, delay=0, utc=False):

        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            # due to non-posix-compliant Windows feature
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1

        t = int(time.time())
        #DBG.info('self.rolloverAt ' + str(self.rolloverAt))
        if t >= self.rolloverAt:
            return 1
        return 0

dbgHandler = SizedTimedRotatingFileHandler(log_file_debug,
                                           maxBytes=100*1024*1024, backupCount=20, 
                                           when=log_when, interval=log_interval)
dbgHandler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)d\t%(threadName)s,\t ' +
                                          '%(levelname)s\tin \'%(module)s\' at line %(lineno)d: \t' +
                                          '%(message)s',
                                          '%Y-%m-%d/%H:%M:%S'))
dbgHandler.setLevel(log_file_debug_level)
DBG.addHandler(dbgHandler)

#ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)
#DBG.addHandler(ch)
DBG.addHandler(dbgHandler)
DBG.setLevel(logging.DEBUG)

#=================================================

LDB = logging.getLogger("database_logger")
ldbHandler = SizedTimedRotatingFileHandler(log_file_database,
                                           maxBytes=log_max_file_size, 
                                           backupCount=log_max_files_count, 
                                           when=log_when, interval=log_interval)
ldbHandler.setFormatter(logging.Formatter(
    "%(asctime)s\tin \'%(module)s\' at line %(lineno)d:\t%(message)s", "%Y-%m-%d/%H:%M:%S"))
LDB.addHandler(ldbHandler)
LDB.setLevel(logging.DEBUG)
LDB.info("test LDB on start")


#=================================================

ERR = logging.getLogger("errors_logger")
errHandler = SizedTimedRotatingFileHandler(log_file_errors,
                                           maxBytes=log_max_file_size, 
                                           backupCount=log_max_files_count, 
                                           when=log_when, interval=log_interval)
errHandler.setFormatter(logging.Formatter(
    "%(asctime)s\tin \'%(module)s\' at line %(lineno)d:\t%(message)s", "%Y-%m-%d/%H:%M:%S"))
ERR.addHandler(errHandler)
#ERR.error("test error on start")


class Error (Enum):
    NO_ERROR = 'NO_ERROR'
    EMPTY_ANSWER = 'ERROR_EMPTY_ANSWER'
    UNEXPECTED = 'UNEXPECTED_ERROR'
    FAILED_SOMETHING = 'ERROR_FAILED_SOMETHING'
    INVALID_TOKEN = 'ERROR_INVALID_TOKEN'
    CANT_START_MMS = 'CANT_START_MMS'
    MMS_NOT_STARTED = 'ERROR_MMS_NOT_STARTED'
    WRONG_CREDENTALS = 'ERROR_WRONG_CREDENTALS'
    CANNOT_CONNECT_TO_MMS = 'ERROR_CANNOT_CONNECT_TO_MMS'
    WAIT_MMS_TIMEOUT = 'ERROR_WAIT_MMS_TIMEOUT'
    CONFIG_ADDRESS = 'ERROR_CONFIG_ADDRESS'
    FLAG_FILE_NOT_EXIST = 'ERROR_FLAG_FILE_NOT_EXIST'
    CONTAINER_NOT_EXIST = 'ERROR_CONTAINER_NOT_EXIST'
    WRONG_INIT_PARAM = 'ERROR_WRONG_INIT_PARAM'
    COULD_NOT_RESOLVE_HOST = 'ERROR_COULD_NOT_RESOLVE_HOST'
'''
#=== ERR log errors ===
WRONG_STOP_MODE
TRY_TO_EXEC_IN_STOPED_CONTAINER
CAN_NOT_EXEC_RUN 
JUNCTIONS_CREATE_EXCEPTION
ERROR_CANNOT_CONNECT_TO_MMS
START_OR_REGISTER_EXCEPTION
ERROR_CONTAINER_NOT_EXIST
HEARTBEAT_EXCEPTION
AUTOSTOP_EXCEPTION1
AUTOSTOP_EXCEPTION2
MAKE_JSON_EXCEPTION
START_LOOP_EXCEPTION
START_PLAN_EXCEPTION
STOP_PLAN_WARNING
TOO_MANY_CONTAINERS_FROM
WORKER_PER_CONTAINER_EXCEPTION
WRONG_FINISH_STEP
WORKER_LOOP_EXCEPTION
LOCK_FILE_ERROR
ERROR_TASK_MANAGER_CONNECTION
CALL_SYNC_EXCEPTION
CONTAINER_NOT_CREATED
WRONG_ARGUMENT_FORMAT
TASKS_EXCEPTION
'''


PRF = logging.getLogger('performance_logger')
prfHandler = SizedTimedRotatingFileHandler(log_file_perf, maxBytes=log_max_file_size, 
                  backupCount=log_max_files_count, when=log_when, interval=log_interval)
prfHandler.setFormatter(
    logging.Formatter(
        '%(asctime)s\t%(message)s',
        '%Y-%m-%d/%H:%M:%S'))
PRF.addHandler(prfHandler)
PRF.setLevel(logging.DEBUG)
# PRF.info('TEST_PERFORMANCE_ON_START')


class Task (Enum):
    PROVISION_AGENT = 'TASK_PROVISION_AGENT'
    WAKEUP_AGENT = 'TASK_WAKEUP_AGENT'
    BACKUP_AGENT = 'TASK_BACKUP_AGENT'


class Stage (Enum):
    CONNECT_MMS = 'STAGE_CONNECT_MMS'
    CONTAINER_CREATE = 'STAGE_CONTAINER_CREATE'
    CONTAINER_START = 'STAGE_CONTAINER_START'
    CONTAINER_REGISTER = 'STAGE_CONTAINER_REGISTER'
    CONTAINER_STOP = 'STAGE_CONTAINER_STOP'


class Operation (Enum):
    WAIT_ZMQ_SESSION = 'OPERATION_WAIT_ZMQ_SESSION'
    WAIT_MMS_INITED = 'OPERATION_WAIT_MMS_INITED'
    WAIT_MMS_CONNECTED = 'OPERATION_WAIT_MMS_CONNECTED'


class StopWatch(object):
    def __init__(self, name: Enum):
        self.name = ''
        if str(type(name)).find('<enum') >= 0:
            self.name = name.value
        if isinstance(name, str):
            self.name = name
        self.startTime = time.time()
        self.params = {}
        DBG.debug('StopWatch ' + self.name + ' created!')

    def addPair(self, name: str, value: str):
        self.params[name] = value

    def stopW(self, success=True, comment: str = ''):
        self.stopTime = time.time()
        self.addPair('success', str(success))
        paramsJoined = ' '
        for key in self.params:
            paramsJoined += key + '=' + self.params[key] + ' '
        PRF.info(str(round(self.stopTime * 1000)) + ' ' + self.name + ' ' +
                 str(round(self.stopTime - self.startTime, 3)) +
                 paramsJoined + comment)
        DBG.debug('StopWatch ' + self.name + ' stoped.')

#sw = StopWatch('TEST_PERFORMANCE_ON_START')
#sw.stopW(True, 'ACC=fake CT_ID=628a370b-c66a-452e-9ca0-4ab20e443ac9')

TIME_MASK = '%Y-%m-%d/%H:%M:%S'

def co(containerId: str, message: str):
  logs_path = 'C:/ProgramData/Acronis/Cloud2Cloud/logs'
  with open(logs_path + '/r_' + containerId + '.log', 'a') as f:
    f.write(time.strptime(time.time(), TIME_MASK) + '\t' + message + '\n')

def debug(message: str, containerId: str = None):
  DBG.debug(message)

def info(message: str, containerId: str = None):
  DBG.debug(message)

def warning(message: str, containerId: str = None):
  DBG.warning(message)
  ERR.warning(message)

