"""
  @file    config.py
  @brief   read config in single place
  @details Copyright (c) 
  @author  Nikolay Vovk
  @since   $Id: $
"""

import json
import time

need_stop_service = False
run_as_service = False

_prefix = '' 

def read():
    namepath = _prefix + 'config.json'
    content = ''
    with open(namepath) as f:
        content = json.load(f)
    return content

def sleep(time_to_sleep):
    i = 0
    while i < time_to_sleep*10 and not need_stop_service:
        time.sleep(0.1)
        i += 1
