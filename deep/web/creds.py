"""
  @file    config.py
  @brief   read config in single place
  @details Copyright (c) 
  @author  Nikolay Vovk
  @since   $Id: $
"""

import requests
import json
from urllib.parse import quote_plus
from tornado.web import RequestHandler, Application, StaticFileHandler
from tornado_http_auth import DigestAuthMixin, BasicAuthMixin, auth_required

import web.logs as logs
DBG = logs.DBG
ERR = logs.ERR

import web.db as db
import web.config as config
cfg = config.read()
credentials = cfg.get('credentials', {
    'user1': 'pass1',
    'user2': 'pass2',
})
