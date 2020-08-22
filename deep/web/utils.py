"""
  @file    utils.py
  @brief   utils for any module
  @details Copyright (c) 
  @author  Nikolay Vovk
"""

import time
import base64
from math import log
import xml.etree.ElementTree as ET

def calctime(func):
    def wrapper(*args, **kwargs):
        a = time.time()
        rez = func(*args, **kwargs)
        b = time.time()
        print(func.__name__ + ' time = ' + str(b-a) + 's')
        return rez
    return wrapper

def to64(s):
    return base64.encodebytes(s.encode()).decode()

def fm64(s):
    return base64.decodebytes(s.encode()).decode()

def int2base64(i):
    bytes_count = int(log(i)/log(256)) + 1
    return base64.encodebytes(i.to_bytes(bytes_count, 'big'))

def base64toInt(b64):
    return int.from_bytes(base64.decodebytes(b64), 'big')

def child_by_name(root, s):
    s = s.lower()
    ch = None
    for child in root:
        tag = child.tag.lower()
        if tag.find(s) > -1:
            ch = child
    return ch
    
def nake(s):
    if s.find('}') > -1:
        return s.split('}')[1]
    return s
            
#=========

def send_xml_file(req, xml_file = 'folders_ret.xml'):
    with open('xml/' + xml_file, 'r') as f:
        txt = f.readlines()
        for line in txt:
            req.write(line.split('\n')[0])

def send_xml_class(req, xml: ET.Element):
    req.write('<?xml version="1.0" encoding="utf-8"?>')
    for line in ET.tostringlist(xml):
        req.write(line.decode())
            
def print_xml(root):
    for line in ET.tostringlist(root):
        DBG.debug(line.decode())
