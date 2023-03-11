class ListTree:
    def __init__(self, root_name) -> None:
        self.root_name = root_name
        self.root = ['root',root_name,[]]
        # all items have identical structure to self.root. all items will be inserted into the empty list. Therefore,
        # we need the index of the empty list, as this will be used for inserting other items
        for i in enumerate(self.root):
            if i[1] == []:
                self.into = i[0]
                

    def add_item(self, parent_path, item_name):
        if parent_path == 'root':
            insert_path = [self.into]
            # count direct root children
            count_children = len(self.root[self.into])
            new_item_path = [count_children]

        else:
            insert_path = self.convert_path(parent_path,'set')
            count_children = len(self.get_item(parent_path)[self.into])
            new_item_path = parent_path
            new_item_path.append(count_children)

        item = [new_item_path, item_name, []]
        self.root = self.set_item(self.root, insert_path, item)

    def convert_path(self,path:list,set_or_get:str):
        new_path = [self.into]
        for i in path:
            new_path.append(i)
            new_path.append(self.into)

        if set_or_get == 'set':
            return new_path
        
        elif set_or_get == 'get':
            new_path.pop()
            return new_path
        
        else:
            return "INVALID ARGUMENT IN .convert_path(): set_or_get MUST EQUAL 'set' OR 'get'.\n"
    
    def set_item(self, lst, path, item, depth=0):
        if depth == len(path) - 1:
            lst[path[depth]].append(item)
            return lst
        else:
            self.set_item(lst[path[depth]], path, item, depth+1)
            return lst
        
    def get_item(self, path):
        # convert path 
        converted_path = self.convert_path(path, 'get')

        def recursive_get(lst, path, depth=0):    
            if depth == len(path) - 1:
                return lst[path[depth]]
            else:
                return recursive_get(lst[path[depth]], path, depth+1)
        
        return recursive_get(self.root, converted_path)
    
    def show(self):
        print(self.root_name)
        def recurs_print_items(tree):
            for item in enumerate(tree):
                if isinstance(item[1], str):
                    depth = len(tree[item[0]-1])
                    print(('   ' * depth) + '•' + item[1])
                elif isinstance(item[1], list):
                    recurs_print_items(item[1])
                    
        recurs_print_items(self.root[2])

        
# test add_item
tree = ListTree('programming')
print(tree.root)
tree.add_item('root','research')
tree.add_item([0],'read')
tree.add_item('root','projects')
tree.add_item('root', 'networking')
tree.add_item([1],'tree to do')

['root', 'programming', [[[0], 'research', [[[0, 0], 'read', []]]]]]
[[0], 'research', [[[0, 0], 'read', []]]]