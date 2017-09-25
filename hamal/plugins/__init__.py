from hamal.utils import ansiblelib
from hamal.db import api as db_api
from hamal.utils import log
import sys

def is_master_head(role, node):
    node_list = db_api.node_get_by_condition_with_order('created_at', role_uuid=role.uuid)
    if None == node_list or 0 == len(node_list):
        log.LOG_CRITICAL('no node belong to role_uuid = %s'%role.uuid)
        sys.exit(0)

    for mynode in node_list:
        if node.uuid == mynode.uuid:
            if mynode == node_list[0]:
                return True
            else:
                return False

    log.LOG_CRITICAL('node is not belong to role_uuid = %s'%role.uuid)

    sys.exit(0)

def is_master_tail(role, node):
    node_list = db_api.node_get_by_condition_with_order('created_at', role_uuid=role.uuid)
    if None == node_list or 0 == len(node_list):
        log.LOG_CRITICAL('no node belong to role_uuid = %s'%role.uuid)
        sys.exit(0)

    for mynode in node_list:
        if node.uuid == mynode.uuid:
            if mynode == node_list[len(node_list)-1]:
                return True
            else:
                return False

    log.LOG_CRITICAL('node is not belong to role_uuid = %s'%role.uuid)

    sys.exit(0)

def get_node_info_list_in_role(role):
     return  db_api.node_get_by_condition_with_order('created_at', role_uuid=role.uuid)

def get_rack_by_uuid(rack_uuid):
    return db_api.rack_get_by_uuid(rack_uuid)


class BasePlugin(object):
    def __init__(self, hosts, path, extra_vars, notexe=False):
        self._ansible = ansiblelib.AnsiblePlay()
        self._hosts = hosts
        self._path = path
        self._extra_vars = extra_vars
        self._notexe = notexe

    def get_hosts(self):
        return self._hosts

    def set_hosts(self, hosts):
        self._hosts = hosts

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def get_extra_vars(self):
        return self._extra_vars

    def set_extra_vars(self, extra_vars):
        self._extra_vars = extra_vars

    def _run(self, *args, **kwargs):
        if True == self._notexe:
            print 'this node do not exe!'
            return
        if None == self._hosts:
            print "hosts is None!"
            sys.exit(0)
        if None == self._path:
            print "path is None!"
            sys.exit(0)
        if None == self._extra_vars:
            print "extra_vars is None!"
            sys.exit(0)
        return self._ansible                            \
                   .set_hosts(self._hosts)              \
                   .set_group(self.__class__.__name__)  \
                   .set_inventory()                     \
                   .set_extra_vars(self._extra_vars)    \
                   .set_play_book(self._path)           \
                   .play()

    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)
