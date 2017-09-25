__author__ = 'midea'

import uuid

def UUIDGEN():
    uuidcls = uuid.uuid1()
    return str(uuidcls)

def UUIDGEN_SIMPLE():
    uuidcls = uuid.uuid1()
    return ''.join(str(uuidcls).split('-'))


if __name__ == '__main__':
    print UUIDGEN()
    print UUIDGEN_SIMPLE()
