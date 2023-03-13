from example_list import root
class ListTree:
    def __init__(self, root_name) -> None:
        self.root_name = root_name
        self.root = ['root',root_name,[]]
        # all items have identical structure to self.root. all items will be inserted into the empty list. Therefore,
        # we need the index of the empty list, as this will be used for inserting other items
        for i in enumerate(self.root):
            if i[1] == []:
                self.into = i[0]
    # converts path used by user to machine readable path   
    
    def create_path(self, address):
        path = [self.into]
        for i in address:
            path.append(i)
            path.append(self.into)
        return path
    
    def select(self, address):
        if address == 'root':
            return self.root[self.into]
        
        else:
            selected_item = self.root
            path = self.create_path(address)     
            for index in enumerate(path):
                if index[0] == len(path) - 1:
                    return selected_item[index[1]]
                else:
                    selected_item = selected_item.__getitem__(index[1])
    
    def count_children(self, parent_address):
        if parent_address == 'root':
            return len(self.root[self.into])
        else:
            return len(self.select(parent_address))
        
    def insert_item(self, parent_address, new_item_name):
        siblings_count = self.count_children(parent_address)
        new_address = parent_address.copy()
        new_address.append(siblings_count)
        new_item = [new_address, new_item_name, []]
        self.select(parent_address).append(new_item)
    
    def insert_node(self, node, new_parent_address, new_rank=0):
        siblings_count = self.count_children(new_parent_address)
        if new_rank > siblings_count or new_rank < 0:
            return 'INVALID NEW RANK'
        # first insert node as the last child of its parent, later we will sort it again
        temporary_rank = siblings_count
        node_address = new_parent_address.copy()
        node_address.append(temporary_rank)
        node[0] = node_address
        self.select(new_parent_address).append(node)
        self.relabel_children(node_address)
        
    def rm(self, item_path):
        parent_address = item_path.copy()
        parent_address.pop()
        position = item_path[-1]
        # remove node from the tree
        detached_node = self.select(parent_address).pop(position)
        # rewrite correct adddresses for each remaining item
        rank = 0
        for i in self.select(parent_address):
            i[0][-1] = rank
            rank += 1
        self.sort_items(parent_address)
        return detached_node
        
    def reposition_item(self, item_address, new_rank):
        current_rank = item_address[-1]
        parent_address = item_address
        parent_address.pop()
        
        if len(parent_address) == 0:
            parent_address = 'root'
        
        item_sibling_count = self.count_children(parent_address)
        
        if current_rank == new_rank:
            return 'NEW RANK CANNOT EQUAL CURRENT RANK'
        
        if new_rank > item_sibling_count or new_rank < 0:
            return "NEW RANK OUTSIDE VALID RANGE"
        # re rank all siblings
        self.select(parent_address)[current_rank][0][-1] = new_rank
        for i in range(new_rank, current_rank):
            self.select(parent_address)[i][0][-1] += 1
        
        print(self.select(parent_address))
        
        self.sort_items(parent_address)
        
    def reparent(self, node_address, new_parent_address):
        node = self.rm(node_address)
        self.insert_node(node, new_parent_address)
        
        
        # sort items now that address information of target items has been changed
    def sort_items(self, parent_address):
        sorted_items = sorted(self.select(parent_address), key=lambda x:x[0][-1])
        for i in range(len(sorted_items)):
            self.select(parent_address)[i] = sorted_items[i]
        for i in self.select(parent_address):
            self.relabel_children(i[0])
        
    def relabel_children(self, parent_address):
        # relabel a parent's children after its own address has been changed.
        def relabel_recurs(item, parent_address_recurs):
            for element in item:
                if isinstance(element, str):
                    # normal case, the parent address has changed, but its length has not changed
                    item[0][0:len(parent_address_recurs)] = parent_address
                    # parent address has increased, 
                    
                    
                elif isinstance(element, list):
                    relabel_recurs(element, parent_address_recurs)
        
        item = self.select(parent_address)
        relabel_recurs(item, parent_address)
                     
        
    def show(self):
        print('**'+self.root_name+'**')
        def recursive_print(lst):
            for i in enumerate(lst):
                if isinstance(i[1], str):
                    indent = ' ' * 4 * len(lst[i[0] - 1])
                    print( indent + '•' + i[1] + f"____{lst[i[0]-1]}")
                elif isinstance(i[1], list):
                    recursive_print(i[1])
        recursive_print(self.root[self.into])
                    
    
                

tree = ListTree('programming')
tree.root = root
tree.insert_item([1,0], 'finish refactor')
tree.insert_item([1,0,0], 'some shit')
tree.insert_item([1,0], 'add reorder function')
tree.insert_item([1,0], 'add detach_and_retach')
tree.insert_item([1], 'testing 123')
tree.insert_item([1], '123')
tree.insert_item([1],'hello again')
tree.insert_item([1,2],' a child')
tree.show()
tree.reposition_item([1,0,2],0)
tree.show()
