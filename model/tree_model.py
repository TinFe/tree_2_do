import json
class ListTree:
    def __init__(self, root_name) -> None:
        self.root_name = root_name
        self.root = ['root',root_name,[]]
        # store indexes for accessing different node elements
        self.index_address = 0
        self.index_node_name = 1
        self.index_child = 2
        # list of nodes used later for displaying the tree
        self.tree_list = []

# ============ Selecting Nodes ============ #
    # `address` is used to access items in the nested list. an address of [1,2,3] will be used in the manner of tree.root[1][2][3]
    # convert address into path than can actually be used to select the node   
    def create_path_to_children(self, address):
        path = [self.index_child]
        for i in address:
            path.append(i)
            path.append(self.index_child)
        # to properly access the list an address of [1,2,3] needs to be converted to [self.index_child, 1, self.index_child, 2, self.index_child, 3, self.index_child]
        return path
    
    # takes node address as argument, selects and returns node from the root
    def select_children(self, node_address):
        if node_address == 'root':
            return self.root[self.index_child]
        else:
            selected_node = self.root
            # convert address to exact path of node in the nested list
            path = self.create_path_to_children(node_address)
            # ex. path of [self.index_child, 1, self.index_child, 2, self.index_child]  ---> tree.root[self.index_child][1][self.index_child][2][self.index_child]  ---> `node object` 
            for index in enumerate(path):
                if index[0] == len(path) - 1:
                    return selected_node[index[self.index_node_name]]
                else:
                    selected_node = selected_node.__getitem__(index[1])
                    
    # get node by address
    # hacky way of getting a node directly, which uses select_children
    def select_node(self, node_address):
        parent_address = node_address.copy()
        parent_address.pop()
        item_index = node_address[-1]
        return self.select_children(parent_address)[item_index]

# ============ Organize/Analyze ============#
    # count children of a given parent, needed for correct addressing and ordering
    def count_children(self, parent_address):
        if parent_address == 'root':
            return len(self.root[self.index_child])
        else:
            return len(self.select_children(parent_address))
        
    # sort items after parent node's children's addresses have been changed
    def sort_items(self, parent_address):
        sorted_items = sorted(self.select_children(parent_address), key=lambda x:x[0][-1])
        for i in range(len(sorted_items)):
            self.select_children(parent_address)[i] = sorted_items[i]
        for i in self.select_children(parent_address):
            self.readdress_children_after_reposition(i[0])
    
    # recursively relablel children's addresses after being repositioned    
    def readdress_children_after_reposition(self, parent_address):
        # relabel a parent's children after its own address has been changed.
        def relabel_recurs(node, parent_address_recurs):
            for element in node:
                if isinstance(element, str):
                    node[0][0:len(parent_address_recurs)] = parent_address
                    # parent address has increased,                     
                elif isinstance(element, list):
                    relabel_recurs(element, parent_address_recurs)
        
        node = self.select_children(parent_address)
        relabel_recurs(node, parent_address)
    
    # relabel node addresses after a node has been reparented
    def readdress_children_after_insert(self, child_node, parent_address):
        for element in child_node:
            # check if the iterator is currently at a node's name item e.g. [[0,0,0], 'some node name' [. . . ]]
            #                                                                          ^^^^^^^^^^^^^^   
            if isinstance(element, str):
                # remove the beginning of the address, leaving only the rank
                del child_node[0][0:len(child_node[0]) - 1]
                parent_address_copy = parent_address.copy()
                # insert the parent address to the beginning of the child address
                for i in range(len(parent_address_copy)):
                    child_node[self.index_address].insert(0,parent_address_copy.pop())
                # set the new parent address equal to the current item's address
                parent_address = child_node[self.index_address]
            elif isinstance(element, list) and element:
                self.readdress_children_after_insert(element, parent_address)
        
# ============ Modify ============ #
    # reparent a node by removing it from the tree and inserting it into another node
    def reparent(self, node_address, new_parent_address):
        # Errors
        # try to reparent a node to itself
        if node_address == new_parent_address:
            return print('CANNOT REPARENT A NODE TO ITSELF')
        # try to reparent a node to one of its own children
        if new_parent_address[0:len(new_parent_address) - 1] == node_address and len(new_parent_address) > len(node_address):
             return print('CANNOT REPARENT A NODE TO ONE OF ITS OWN CHILDREN')
        # check if removing the node to be inserted will change the index of the parent node
        if new_parent_address[0:len(node_address) - 1] == node_address[0:len(node_address) - 1] and node_address[-1] < new_parent_address[len(node_address) - 1]:
            new_parent_address[len(node_address) - 1] -= 1
        node = self.rm(node_address)
        self.insert_node(node, new_parent_address)
        
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
        self.select_children(parent_address)[current_rank][self.index_address][-1] = new_rank
        if new_rank > current_rank:
            for i in range(current_rank + 1, new_rank + 1):
                self.select_children(parent_address)[i][self.index_address][-1] -= 1
        elif new_rank < current_rank:
            for i in range(new_rank, current_rank):
                self.select_children(parent_address)[i][self.index_address][-1] += 1
        
        self.sort_items(parent_address)
    
    # remove a node   
    def rm(self, item_path):
        parent_address = item_path.copy()
        parent_address.pop()
        position = item_path[-1]
        # remove node from the tree
        detached_node = self.select_children(parent_address).pop(position)
        # rewrite correct adddresses for each remaining item
        rank = 0
        for i in self.select_children(parent_address):
            i[self.index_address][-1] = rank
            rank += 1
        self.sort_items(parent_address)
        return detached_node

    def rename_node(self, node_address, new_name):
        item = self.select_node(node_address)
        item[self.index_node_name] = new_name
    
    # create and insert a new item into a chosen parent node. parent node is selected by address    
    def new_node(self, parent_address, new_item_name):
        # count children of parent node you are inserting into. the count will be used for the new_item's address. if the parent node has 
        # 2 children (child 0 and child 1), the last index of the new item's address will be 2.
        siblings_count = self.count_children(parent_address)
        # all but the last index of the new_item address are the same as its parent's
        new_item_address = parent_address.copy()
        new_item_address.append(siblings_count)
        # create new item
        new_item = [new_item_address, new_item_name, []]
        # append new item to its parent
        self.select_children(parent_address).append(new_item)
        # reposition new item so that it is the 0th element of its parent (copying the new_item_address prevents 
        # bad things I don't understand from happening)
        new_item_address_copy = new_item_address.copy() 
        self.reposition_item(new_item_address_copy, 0)
    
    # insert node ojbect into a parent node. 
    def insert_node(self, node, new_parent_address, new_rank=0): 
        siblings_count = self.count_children(new_parent_address)
        if new_rank > siblings_count or new_rank < 0:
            return 'INVALID NEW RANK'
        # first insert node as the last child of its parent, later we will sort it again
        temporary_rank = siblings_count
        # node will have a new address. we create it here. 
        node_address = new_parent_address.copy()
        node_address.append(temporary_rank)
        # change the address of the node we are inserting
        node[0] = node_address
        # append node to the parent
        self.select_children(new_parent_address).append(node)
        # re-address newly inserted node's children
        self.readdress_children_after_insert(node[self.index_child], node_address)
        node_address_copy = node_address.copy()
        # reorder node to desired position (0 by default)
        self.reposition_item(node_address_copy, new_rank)
            
# ============ Save, Load and Display ============ # 
    # show tree, including each node's address indenting according to how 'deep' in the tree an item is
    def show(self):
        print('**'+self.root[1]+'**')
        def recursive_print(lst):
            for i in enumerate(lst):
                if isinstance(i[1], str):
                    indent = ' ' * 4 * len(lst[i[0] - 1])
                    print( indent + '•' + i[1] + f"____{lst[i[0]-1]}")
                elif isinstance(i[1], list):
                    recursive_print(i[1])
        recursive_print(self.root[self.index_child])
        
    # add every item in the tree, one by one, in order, to self.tree_list
    def make_tree_list(self):
        self.tree_list = []
        tree_list_header = {'item_text':'**'+self.root[1]+'**','item_address':'root'}
        self.tree_list.append(tree_list_header)
        def recursive_append(lst):
            for i in enumerate(lst):
                if isinstance(i[1], str):
                    indent = ' ' * 8 * len(lst[i[0] - 1])
                    item = {'item_text':indent + '•' + i[1], 'item_address':lst[i[0] - 1]}
                    self.tree_list.append(item)
                elif isinstance(i[1], list):
                    recursive_append(i[1])
        recursive_append(self.root[self.index_child])
        return self.tree_list
    
    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.root, f)
    
    def load(self, filename):
        with open(filename, 'r') as f:
            self.root = json.load(f)
            
            
