# -*- coding:utf-8 -*-
from auto_openstack.util.log import LOG_CRITICAL
from auto_openstack.util import xmltodict
import json
import os

def load_file(filename):
    fileobj = None
    all_text  = ""
    try:
        fileobj = open(filename, 'rb')
        all_text = fileobj.read( )
    except IOError, why:
        LOG_CRITICAL("IO error! %s" % why)
        raise Exception("IO error! %s" % why)
    finally:
        if None != fileobj:
            fileobj.close( )
    return all_text

def load_file_by_type(filename, type='json'):
    if type not in ['json', 'xml']:
        return None
    fileobj = None
    all_text  = ""
    try:
        fileobj = open(filename, 'rb')
        all_text = fileobj.read( )
    except IOError, why:
        LOG_CRITICAL("IO error! %s" % why)
        raise Exception("IO error! %s" % why)
    finally:
        if None != fileobj:
            fileobj.close( )
    if 'xml' == type:
        try:
            root = xmltodict.parse(all_text,encoding='utf-8',
                force_list=['nodes','interfaces','bridges','route','rule','disks','roles','components'])
        except KeyboardInterrupt, why:
            raise Exception("IO error! %s" % why)
        try:
            all_text = json.dumps(root['root'])
        except KeyboardInterrupt, why:
            raise Exception("IO error! %s" % why)

    return all_text

def write_file(path, alltext):
    try:
        exist = os.path.exists(os.path.dirname(path))
        if False == exist:
            os.makedirs(os.path.dirname(path))
    except OSError, why:
        raise Exception("%s path operate error! %s" % (os.path.dirname(path), why))

    fileobj = None
    try:
        fileobj = open(path, 'w')
        fileobj.write(alltext)
    except IOError, why:
        LOG_CRITICAL("IO error! %s" % why)
        raise Exception("IO error! %s" % why)
    finally:
        if None != fileobj:
            fileobj.close( )

    try:
        os.chmod(path, 0644)
    except OSError, why:
        raise Exception("chmod operate error! %s" %  why)

