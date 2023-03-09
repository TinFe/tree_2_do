# sample: [level, index_of_level, item_name, sub_item_array]
to = 2
root = ['_','programming',[]]
root[to].append([[0],'research',[]])
root[to].append([[1],'projects',[]])
root[to].append([[2],'networking',[]])
root[to][1][to].append([[1,0],'tree to do',[]])
root[to][0][to].append([[0,0],'read book',[]])
root[to][2][to].append([[2,0],'go to meetup',[]])
root[to][1][to].append([[1,1],'mandelbrot',[]])
root[to][1][to][0][to].append([[1,0,0],'create tree class using nested lists',[]])

def print_tree(tree, indent=0):
    for item in tree:
        if isinstance(item, list):
            print_tree(item, indent+1)
        else:
            print(" " * 4 * indent + item[1])

print_tree(root)
