class ListTree:
    def __init__(self, root_name) -> None:
        self.root_name = root_name
        self.root = ['_','programming',[]]
        # all items have identical structure to self.root. all items will be inserted into the empty list. Therefore,
        # we need the index of the empty list, as this will be used for inserting other items
        for i in enumerate(self.root):
            if i[1] == []:
                self.into = i[0]

    def add_item(self, path, item_name):
        if path == 0:
            insert_path = [self.into]
        else:
            insert_path = self.convert_insert_path(path)

        print(insert_path)
        item = ['_', item_name, []]
        self.root = self.set_item(self.root, insert_path, item)

    def convert_insert_path(self,path:list):
        new_path = [self.into]
        for i in path:
            new_path.append(i)
            new_path.append(self.into)
        return new_path

    def set_item(self, lst, path, item, depth=0):
        if depth == len(path) - 1:
            lst[path[depth]].append(item)
            return lst
        else:
            self.set_item(lst[path[depth]], path, item, depth+1)
            return lst

# test add_item
tree = ListTree('programming')
print(tree.root)
tree.add_item(0,'research')