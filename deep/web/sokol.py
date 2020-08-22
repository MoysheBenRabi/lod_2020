"""
  @file    config.py
  @brief   read config in single place
  @details Copyright (c) 
  @author  Nikolay Vovk
  @since   $Id: $
"""

from web.network import Network 
import csv

nw = Network()

def main(write):
    write('<html><body>SOkol<body/><html/>')

def init(write):
    nw.init()
    write('deep network inited')

def iter(write):
    ls = nw.read_test_line()
    s = ''
    for w in ls:
        s += str(w) + ','
    write(s)

def manu(write):
    s = nw.get_full_info()
    write(s)

def auto(write):
    s = nw.get_playbook()
    write(s)