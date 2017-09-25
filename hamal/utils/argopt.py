import argparse

class ArgOpt(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        self.args = None

    def add_arg(self, short, long, help, type=str, hasarg=True):
        if True == hasarg:
            if int == type:
                self.parser.add_argument('-%s'%short,'--%s'%long, help=help, type=int)
            else:
                self.parser.add_argument('-%s'%short,'--%s'%long, help=help, type=str)
        else:
            self.parser.add_argument('-%s'%short,'--%s'%long, help=help, action='store_true')

    def get_arg_value_by_name(self, long):
        if None is self.args:
            self.args = self.parser.parse_args()
        return eval('self.args.%s'%long)


if __name__ == '__main__':
    argopt = ArgOpt()
    argopt.add_arg('t', 'test', 'this is a test!', hasarg=False)
    argopt.add_arg('m', 'module', 'this is a module!', hasarg=True)

    print argopt.get_arg_value_by_name('test')
    print argopt.get_arg_value_by_name('module')




