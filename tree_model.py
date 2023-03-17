import json
class ListTree:
    def __init__(self, root_name) -> None:
        self.root_name = root_name
        self.root = ['root',root_name,[]]
        # all items have identical structure to self.root. all items will be inserted into the empty list. Therefore,
        # we need the index of the empty list, as this will be used for inserting other items
        self.into = 0
        for i in enumerate(self.root):
            if i[1] == []:
                self.into = i[0]
        self.tree_string = ''
    # `address` is used to access items in the nested list. an address of [1,2,3] will be used in the manner of tree.root[1][2][3]
    # converts address used by user to code readable path   
    def create_path(self, address):
        path = [self.into]
        for i in address:
            path.append(i)
            path.append(self.into)
        # to properly access the list an address of [1,2,3] needs to be converted to [self.into, 1, self.into, 2, self.into, 3, self.into]
        return path
    
    # takes node address as argument, selects and returns node from the root
    def select(self, address):
        if address == 'root':
            return self.root[self.into]
        else:
            selected_item = self.root
            # convert address to usable path
            path = self.create_path(address)
            # ex. path of [self.into, 1, self.into, 2, self.into]  ---> tree.root[self.into][1][self.into][2][self.into]  ---> `node object` 
            for index in enumerate(path):
                if index[0] == len(path) - 1:
                    return selected_item[index[1]]
                else:
                    selected_item = selected_item.__getitem__(index[1])
                    
    # count children of a given parent, needed for correct addressing and ordering
    def count_children(self, parent_address):
        if parent_address == 'root':
            return len(self.root[self.into])
        else:
            return len(self.select(parent_address))
    
    # insert a new item into a chosen parent node. parent node is selected by address    
    def insert_item(self, parent_address, new_item_name):
        # count children of parent node you are inserting into to give the new item a new address
        siblings_count = self.count_children(parent_address)
        # all but the last elements of the new_item  address are the same as its parent's
        new_address = parent_address.copy()
        new_address.append(siblings_count)
        # create new item
        new_item = [new_address, new_item_name, []]
        self.select(parent_address).append(new_item)
    
    # insert node into another parent node. parent node is selected by address
    def insert_node(self, node, new_parent_address, new_rank=0): 
        siblings_count = self.count_children(new_parent_address)
        if new_rank > siblings_count or new_rank < 0:
            return 'INVALID NEW RANK'
        # first insert node as the last child of its parent, later we will sort it again
        temporary_rank = siblings_count
        # node will have a new address. we create it here. 
        node_address = new_parent_address.copy()
        node_address.append(temporary_rank)
        node[0] = node_address
        # append node to the parent
        self.select(new_parent_address).append(node)
        self.relabel_after_insert(node[self.into], node_address)
        node_address_copy = node_address.copy()
        # reorder node to desired position (0 by default)
        self.reposition_item(node_address_copy, new_rank)
    
    # relabel items after a node has been reparented
    def relabel_after_insert(self, child_node, parent_address):
        for element in child_node:
            if isinstance(element, str):
                # remove the beginning of the address, leaving only the rank
                del child_node[0][0:len(child_node[0]) - 1]
                parent_address_copy = parent_address.copy()
                # insert the parent address to the beginning of the child address
                for i in range(len(parent_address_copy)):
                    child_node[0].insert(0,parent_address_copy.pop())
                # set the new parent address equal to the current item's address
                parent_address = child_node[0]
            elif isinstance(element, list) and element:
                self.relabel_after_insert(element, parent_address)
     
     # remove a node   
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
    
    #  move a node to a different position without changing parent
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
        if new_rank > current_rank:
            for i in range(current_rank + 1, new_rank + 1):
                self.select(parent_address)[i][0][-1] -= 1
        elif new_rank < current_rank:
            for i in range(new_rank, current_rank):
                self.select(parent_address)[i][0][-1] += 1
        
        self.sort_items(parent_address)
        
    def reparent(self, node_address, new_parent_address):
        node = self.rm(node_address)
        self.insert_node(node, new_parent_address)    
        
    # sort items after parent node's children's addresses have been changed
    def sort_items(self, parent_address):
        sorted_items = sorted(self.select(parent_address), key=lambda x:x[0][-1])
        for i in range(len(sorted_items)):
            self.select(parent_address)[i] = sorted_items[i]
        for i in self.select(parent_address):
            self.relabel_children(i[0])
    
    # recursively relablel children's addresses after being repositioned    
    def relabel_children(self, parent_address):
        # relabel a parent's children after its own address has been changed.
        def relabel_recurs(node, parent_address_recurs):
            for element in node:
                if isinstance(element, str):
                    node[0][0:len(parent_address_recurs)] = parent_address
                    # parent address has increased, 
                    
                    
                elif isinstance(element, list):
                    relabel_recurs(element, parent_address_recurs)
        
        node = self.select(parent_address)
        relabel_recurs(node, parent_address)

    # show tree, indenting according to how 'deep' in the tree an item is
    def show(self):
        print('**'+self.root[1]+'**')
        def recursive_print(lst):
            for i in enumerate(lst):
                if isinstance(i[1], str):
                    indent = ' ' * 4 * len(lst[i[0] - 1])
                    print( indent + '•' + i[1] + f"____{lst[i[0]-1]}")
                elif isinstance(i[1], list):
                    recursive_print(i[1])
        recursive_print(self.root[self.into])
    
    def tree_to_str(self):
        self.tree_string = '**'+self.root[1]+'**'
        def write_to_string(lst):
            for i in enumerate(lst):
                if isinstance(i[1], str):
                    indent = ' ' * 4 * len(lst[i[0] - 1])
                    self.tree_string += '\n' + indent + '•' + i[1]
                elif isinstance(i[1], list):
                    write_to_string(i[1])
        write_to_string(self.root[self.into])
        return self.tree_string
    
    def save(self, filename):
        filename = filename + '.json'
        with open(filename, 'w') as f:
            json.dump(self.root, f)
    
    def load(self, filename):
        with open(filename, 'r') as f:
            self.root = json.load(f)
                       


tree = ListTree('')
tree.load('test.json')
s = tree.tree_to_str()
