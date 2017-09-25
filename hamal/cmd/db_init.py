__author__ = 'YANGYQ11'

from hamal.db import migration
from hamal.db import api as db_api
from hamal.utils import argopt
import sys

def main():
    myargopt = argopt.ArgOpt()
    myargopt.add_arg('o', 'opt', 'two opt: db_sync, db_drop', hasarg=True)
    opt = myargopt.get_arg_value_by_name('opt')

    if None == opt or opt not in ['db_sync', 'db_drop']:
        print 'Error: Wrong db opt, please input db_sync or db_drop!'
        sys.exit(0)
    if opt in ['db_sync']:
        migration.create_all_table(db_api.get_engine())
    else:
        migration.drop_all_table(db_api.get_engine())
