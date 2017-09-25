# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext import declarative
from sqlalchemy import Index
from sqlalchemy.sql.schema import ForeignKey

Base = declarative.declarative_base()

### OK
class TableBase():
    from datetime import datetime
    created_at = Column('created_at', DateTime, default=datetime.now())
    updated_at = Column('updated_at', DateTime, default=datetime.now())

### OK
class Region(Base, TableBase):
    __tablename__ = "region"
    __table_args__ = (
        Index('uuid', 'uuid', unique=True),
    )

    id = Column(Integer, primary_key=True, autoincrement=True) #Column
    uuid = Column(String(36))
    name = Column(String(64))  # region name
    pos = Column(String(64))   # region pos
    desc = Column(String(255)) # region desc


### OK
class Rack(Base, TableBase):
    __tablename__ = "rack"
    __table_args__ = (
        Index('uuid', 'uuid', unique=True),
    )

    id = Column(Integer, primary_key=True, autoincrement=True) #Column
    uuid = Column(String(36))
    name = Column(String(64))  # rack name
    num  = Column(Integer)      # rack num
    rack_size = Column(Integer) # How many U in this rack?
    desc = Column(String(255))  # rack desc


### FIXME
class Node(Base, TableBase):
    __tablename__ = "node"
    __table_args__ = (
        Index('uuid', 'uuid', unique=True),
    )
    id = Column(Integer, primary_key=True, autoincrement=True) #Column
    uuid = Column(String(36))
    name = Column(String(64))
    mytype = Column(String(8)) ## pm or vm

    status = Column(Integer) ###  0, noinstall 1, installed
    step = Column(String(255))  ###  'step': '' or role act

### user
    host = Column(String(32))
    port = Column(String(8))
    user =  Column(String(32))
    passwd = Column(String(32))
###

### role
    rack_uuid   = Column(String(36), ForeignKey('rack.uuid'), index=True)
    role_uuid   = Column(String(36), ForeignKey('role.uuid'), index=True)
### role

### cpu
    cpu_arch = Column(String(32))
    cpu_cores = Column(Integer)
    cpu_count = Column(Integer)
    cpu_threads_per_core = Column(Integer)
    cpu_vcpus = Column(Integer)
### cpu

### memory
    memory_mb = Column(Integer)
### memory

### network
    netdev_list = Column(Text)     ###(json)
### network

### disk
    diskdev_map = Column(Text)    ###(json)
    diskdev_blist = Column(Text)  ###(json) # format like this: sdb,sdc
### disk

### os
    os_dist =  Column(String(32))
    os_major_version = Column(String(32))
    os_version = Column(String(32))
    os_release = Column(String(32))
    os_kernel = Column(String(32))
### os

### ok
class Role(Base, TableBase):
    __tablename__ = "role"
    __table_args__ = (
        Index('uuid', 'uuid', unique=True),
    )

    id = Column(Integer, primary_key=True, autoincrement=True) #Column
    uuid = Column(String(36))
    name = Column(String(64))        # role name
    desc = Column(String(255))       # role desc
    myorder = Column(Integer)        # role action execute order
    act_list = Column(Text)          # role action (json)
    mytype = Column(String(36))        # role network type: common|compute|controll|network|storage

class Relation(Base, TableBase):
    __tablename__ = "relation"
    __table_args__ = (
        Index('uuid', 'uuid', unique=True),
    )

    id = Column(Integer, primary_key=True, autoincrement=True) #Column
    uuid = Column(String(36))
    role_uuid   = Column(String(36), index=True)
    node_uuid   = Column(String(36), index=True)
