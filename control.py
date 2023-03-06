
import xml.etree.ElementTree as ET

class Tree:
    def __init__(self,root_name, filename='create_desired_structure.xml'):
        self.root = ET.Element(f'{root_name}', {'id':'0'})
        self.filename = filename
        self.save_to_file(self.root)

    def add_item(self, parent_id, item_name):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        
        # if adding to root:
        if parent_id == '0':
            # get siblings
            siblings = []
            for e in root.iter():
                if len(self.parse_id(e.attrib['id'])) == 2:
                    siblings.append(self.parse_id(e.attrib['id'])[-1])
            if len(siblings) == 0:
                item_id = '1.0'
            else:
                item_id = '1.' + str(max(siblings)+1)
            item = ET.SubElement(root, 'item', {'id':item_id})
        item.text = item_name
        self.save_to_file(root)
    
    def save_to_file(self, root):
        filename = self.filename
        tree = ET.ElementTree(root)
        tree.write(filename)

    def get_element_by_id(self,id):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        selected_element = root.find(f"./*[@id='{id}']")
        return selected_element
    
    def parse_id(self, id):
        id_list = id.split('.')
        for i in enumerate(id_list):
            id_list[i[0]] = int(i[1])
        return id_list
        


tree = Tree('programming')
tree.add_item('0','research\n')
tree.add_item('0','projects\n')
tree.add_item('0','networking\n')

















""""

        self.items = []

    def add_item(self, parent_id, item_name, id):
        if parent_id == '0':
            item = ET.SubElement(self.root, 'item', {'id': f'{id}'})
        else:
            parent = self.get_element(parent_id)
            print(parent)
            item = ET.SubElement(parent, 'item', {'id': f'{id}'})
            item.text = item_name 
        self.items.append(item)
    
    def get_element(self, id):
        print(f'root node is {self.root}')
        selected_element = self.root.find(f"./*[@id='{id}']")
        print(selected_element)
        return selected_element

    def print_xml(self):
        print(root.tag)
        for i in self.root.iter():
            if i.text != None:
                indent = '  ' * int(i.attrib['id'][0])
                print(indent + i.text)
                print(indent + i.attrib['id'])
        

class Item:
    def __init__(self, parent, name, id):
        self.parent = parent
        self.name = name
        self.id = id
        self = 'an object made out of the above elements'


def create_root(root_name):
    root = ET.Element(f'{root_name}',{'id':'0'})
    return root

def get_element(root_node, id):
    selected_element = root_node.find(f"./*[@id='{id}']")
    return selected_element

def add_element(root_node, parent_id, child_name, child_id):
    parent = get_element(root_node,parent_id)


def print_xml(root_node):
    print(root.tag)
    for i in root_node.iter():
        if i.text != None:
            indent = '  ' * int(i.attrib['id'][0])
            print(indent + i.text)
            print(indent + i.attrib['id'])
"""