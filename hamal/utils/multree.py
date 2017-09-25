
class MulTreeNode(object):
    def __init__(self, name, id, children_obj_list):
        self.name = name
        self.id = id
        if None == children_obj_list:
            self.children_obj_list = []
        else:
            self.children_obj_list = children_obj_list

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_children(self):
        return self.children_obj_list

    def append(self, node):
        self.children_obj_list.append(node)

    def remove(self, node):
        self.children_obj_list.remove(node)

    def find_child_by_id(self, id):
        for child in self.children_obj_list:
            if id == child.get_id():
                return child
        return None

    def find_child_by_name(self, name):
        for child in self.children_obj_list:
            if name == child.get_name():
                return child

        return None



class MulTree(object):
    def __init__(self):
        self.root = MulTreeNode('root', 0, None)

    def append_by_name_path(self, node, name_path_list=None):
        cur_node = self.root
        for name in name_path_list:
            tmp = cur_node.find_child_by_name(name)
            if None == tmp:
                return False
            cur_node = tmp
        cur_node.append(node)
        return True

    def append_by_id_path(self, node, id_path_list=None):
        cur_node = self.root
        for id in id_path_list:
            tmp = cur_node.find_child_by_id(id)
            if None == tmp:
                return False
            cur_node = tmp
        cur_node.append(node)
        return True

    def remove_by_name_path(self, node, name_path_list=None):
        cur_node = self.root
        for name in name_path_list:
            tmp = cur_node.find_child_by_name(name)
            if None == tmp:
                return False
            cur_node = tmp
        cur_node.remove(node)
        return True

    def remove_by_id_path(self, node, id_path_list):
        cur_node = self.root
        for id in id_path_list:
            tmp = cur_node.find_child_by_id(id)
            if None == tmp:
                return False
            cur_node = tmp
        cur_node.append(node)
        return True

    def search_by_name(self, name_path_list=None):
        cur_node = self.root
        for name in name_path_list:
            tmp = cur_node.find_child_by_name(name)
            if None == tmp:
                return None
            cur_node = tmp
        return cur_node

    def search_by_id(self, id_path_list=None):
        cur_node = self.root
        for id in id_path_list:
            tmp = cur_node.find_child_by_id(id)
            if None == tmp:
                return None
            cur_node = tmp
        return cur_node

    def foreach_all(self, callback_func):
        stack = []
        stack.append(self.root)
        while 0 < len(stack):
            node = stack.pop()
            callback_func(node)

            for elem in node.get_children():
                stack.append(elem)

def callback_func(node):
    print '========== %s'%node.get_name()
    for elem in node.get_children():
        print 'I am elem: %s'%elem.get_name()

if __name__ == '__main__':
    tree = MulTree()
    id_path_list = []
    for i in xrange(10):
        tree.append_by_id_path(MulTreeNode('===== %d +++++++'%i, i, None),id_path_list)
        id_path_list.append(i)

    id_path_list = [0,1,2]
    tree.append_by_id_path(MulTreeNode('===== %d +++++++'%100, 100, None),id_path_list)

    tree.foreach_all(callback_func)
    print 'jjjj'+tree.search_by_name(['===== 0 +++++++','===== 1 +++++++']).name

