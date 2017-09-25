from prettytable import PrettyTable

class PrettyPrint(object):
    def __init__(self, title_list):
        self._table = PrettyTable(title_list)

    def add_row(self, row_list):
        self._table.add_row(row_list)

    def order_by(self, title):
        self._table.sort_key(title)
        self._table.reversesort = True

    def print_pretty(self):
        print self._table


if __name__ == '__main__':
    import random
    pp = PrettyPrint(['id', 'name', 'score'])

    for i in xrange(10):
        pp.add_row([random.uniform(10,20), str(i)+"wori", random.uniform(10,20)])

    pp.order_by('score')
    pp.print_pretty()

