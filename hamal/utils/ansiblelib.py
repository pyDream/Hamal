#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ansible import constants as C
from ansible import playbook
from ansible import inventory
from ansible import runner as ansible_runner
from ansible import utils
from ansible import callbacks
#from common.log import *


"""
  回调基类
"""
class AnsibleRunnerCB(callbacks.PlaybookRunnerCallbacks):
    pass
'''
    def on_unreachable(self, host, results):
        pass

    def on_failed(self, host, results, ignore_errors=False):
        pass

    def on_ok(self, host, host_result):
        pass

    def on_skipped(self, host, item=None):
        pass

    def on_no_hosts(self):
        pass

    def on_async_poll(self, host, res, jid, clock):
        pass

    def on_async_ok(self, host, res, jid):
        pass

    def on_async_failed(self, host, res, jid):
        pass

    def on_file_diff(self, host, diff):
        pass
'''

class AnsiblePlay(object):
    def __init__(self):
        self._stats = callbacks.AggregateStats()
        self._playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        self._runner_cb = None
        self._inventory = inventory.Inventory()
        self._hosts = []
        self._only_tags = ['all']
        self._skip_tags = []
        self._extra_vars = {}
        self._remote_user = C.DEFAULT_REMOTE_USER
        self._remote_pass = C.DEFAULT_REMOTE_PASS
        self._remote_port = 22
        self._group = None
        self._playbook = None
        self._runner = None
    
    def set_host(self, host, port = 22, ansible_ssh_user=None, ansible_ssh_pass=None, ansible_ssh_private_key_file=None):
        if host:
            inv_host = inventory.Host(
            host, port                          
            )
            if None != ansible_ssh_user:
                inv_host.set_variable('ansible_ssh_user', ansible_ssh_user) 
            if None != ansible_ssh_pass:
                inv_host.set_variable('ansible_ssh_pass', ansible_ssh_pass) 
            if None != ansible_ssh_private_key_file:
                inv_host.set_variable('ansible_ssh_private_key_file', ansible_ssh_private_key_file) 
            if inv_host:
                self._hosts.append(inv_host)
        return self
    
    def set_remote_user(self, username):
        if username:
            self._remote_user = username
        return self
    
    def set_remote_pass(self, password):
        if password:
            self._remote_pass = password
        return self    
            
    def set_remote_port(self, port): 
        if port > 0:
            self._remote_port = port
        return self
    
    def set_hosts(self, hosts):
        if hosts and len(hosts) > 0:
            for host in hosts:
                host_ip   = host.get('host_ip', None)
                host_port = host.get('host_port', 22)

                host_user = host.get('host_user', None)
                host_pass = host.get('host_pass', None)
                host_file = host.get('host_file', None)

                inv_host  = inventory.Host(host_ip, host_port)

                if None != host_user:
                    inv_host.set_variable('ansible_ssh_user', host_user)
                if None != host_pass:
                    inv_host.set_variable('ansible_ssh_pass', host_pass)
                if None != host_file:
                    inv_host.set_variable('ansible_ssh_private_key_file', host_file)
 
                if inv_host:
                    self._hosts.append(inv_host)
        return self
    def get_hosts(self):
        return self._hosts
    
    """
     name为组名，必须指定，对应在yml文件中配置 的hosts
    """        
    def set_group(self, name):
        self._group = inventory.Group(
                 name                      
                )
        """向group中添加host"""
        map(lambda host: self._group.add_host(host), [host for host in self._hosts if self._hosts and len(self._hosts)>0])
        """设置yml执行hosts变量"""
        self._extra_vars['hosts'] = name
        return self
    
    def set_inventory(self):
        if self._group:
            self._inventory.add_group(self._group)
        return self

    def get_inventory(self):
        return self._inventory
    
    def set_only_tags(self, only_tags):
        if only_tags and len(only_tags):
            self._only_tags = only_tags
        return self
    
    def set_skip_tags(self, skip_tags):
        if skip_tags and len(skip_tags):
            self._skip_tags = skip_tags
        return self
    
    def set_extra_vars(self, extra_vars):
        if extra_vars and isinstance(extra_vars, dict):
            for k,v in extra_vars.iteritems():
                self._extra_vars.setdefault(k,v)
        return self
    
    def set_runner_cb(self, runner_cb):
        self._runner_cb = runner_cb
        return self
    
    def set_play_book(self, yamlpath):
        if yamlpath and os.path.isfile(yamlpath):
            self._runner_cb = AnsibleRunnerCB(self._stats)
            self._playbook = playbook.PlayBook(
                playbook = yamlpath,
                stats = self._stats,
                callbacks = self._playbook_cb,
                runner_callbacks = self._runner_cb,
                inventory =  self._inventory,
                only_tags = self._only_tags,
                skip_tags = self._skip_tags,
                extra_vars = self._extra_vars,
                remote_user = self._remote_user,
                remote_pass = self._remote_pass,
                remote_port = self._remote_port
                )
            return self
        else:
#            LOG_ERROR("%s is not found" % yamlpath)
            pass
            
    def play(self):
        if self._playbook:
            res = self._playbook.run()
#            LOG_INFO('%s running result: %s' % (self._group.name, res))
#            print res
            return res
        else:
            return None
    
    def set_runner(self):
        self._runner = ansible_runner.Runner(
				forks=10, pattern='auto_openstack_gather',
                    inventory =  self._inventory,
    				module_name='setup'#, module_args='crontab -l'
		       )
        return self

    def run(self):
        if self._runner:
            res = self._runner.run()
#            print res
            return res

        return None


if __name__ == '__main__':
#   host, port = 22, ansible_ssh_user=None, ansible_ssh_pass=None, ansible_ssh_private_key_file=None
    path = './playbooks/ping.yml'
    extra_vars = dict()
    extra_vars ['extra_deson'] = 'deson is ok'
    '''执行方法'''
    hosts=[
               {
                     "host_ip": "10.16.75.69",
                     "host_user": "root",
                     "host_pass": "Midea@123"
               }
          ]
    hosts1=[
               {
                    "host_ip": "10.16.75.69",
                    "host_user": "root",
                    "host_pass": "Midea@123"
               },
               {
                     "host_ip": "10.16.75.70",
                     "host_user": "root",
                     "host_pass": "Midea@123"
               }
          ]

#    AnsiblePlay().set_hosts(hosts) \
#    .set_group('deson').set_inventory().set_extra_vars(extra_vars).set_play_book(path).play()
    AnsiblePlay().set_hosts(hosts).set_group('ansible_gateway').set_inventory().set_extra_vars(extra_vars).set_runner().run()

#    AnsiblePlay().set_hosts(hosts1).set_group('ansible_gateway').set_inventory().set_extra_vars(extra_vars).set_runner().run()

#    print ROOT_PATH
