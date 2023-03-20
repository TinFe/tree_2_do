import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from tree_model import ListTree, l

# create a MainWindow class
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = qtw.QWidget()
        main_widget.setLayout(qtw.QVBoxLayout())
        self.setCentralWidget(main_widget)
        
        # control panel buttons
        self.control_panel = qtw.QWidget()
        self.control_panel.setLayout(qtw.QHBoxLayout())
        self.insert_item_button = qtw.QPushButton('+')
        self.reposition_item_button = qtw.QPushButton('Reposition')
        self.reparent_node_button = qtw.QPushButton('Reparent')
        self.insert_item_button.clicked.connect(self.insert_item)  
        self.reparent_node_button.clicked.connect(self.reparent_node)
        self.control_panel.layout().addWidget(self.insert_item_button)
        self.control_panel.layout().addWidget(self.reposition_item_button)
        self.control_panel.layout().addWidget(self.reparent_node_button)
        
        # menu bar 
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        new_action = qtg.QAction('New', self)
        open_action = qtg.QAction('Open', self)
        save_action = qtg.QAction('Save', self)
        save_as_action = qtg.QAction('Save As...', self)
        # keyboard shortcuts
        save_action.setShortcut(qtg.QKeySequence.StandardKey.Save)
        open_action.setShortcut(qtg.QKeySequence.StandardKey.Open)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        
        
        

        open_action.triggered.connect(self.load)
        save_action.triggered.connect(self.save)
        
        
        
        
        # reposition variables
        self.reposition_item_button_mode = "initial_press"
        self.reposition_item_new_rank = None
        
        # reparent variables
        self.reparent_node_button_mode = 'initial_press'
        self.reparent_node_address = None
        
        # tree model
        self.tree_file_str = 'test.json'
        self.tree_object = ListTree('_')
        self.tree_object.load(self.tree_file_str)
        self.tree_object.make_tree_list()
        
        # list widget
        self.list_widget = qtw.QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget_font = qtg.QFont()
        self.list_widget_font.setPointSize(18)
        self.list_widget.setFont(self.list_widget_font)
        self.list_widget.setDragEnabled(True)
        
        self.list_widget.itemClicked.connect(self.on_item_click)
        self.backspace = qtg.QShortcut(qtg.QKeySequence(qtc.Qt.Key.Key_Backspace), self)
        self.backspace.activated.connect(self.remove_node)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_click)
        self.list_widget.itemChanged.connect(self.finish_editing_item)
        self.reposition_item_button.clicked.connect(self.reposition_item)
        
        main_widget.layout().addWidget(self.control_panel)
        main_widget.layout().addWidget(self.list_widget)
        
        self.populate_list_widget()
        
        self.show()
        
    def populate_list_widget(self):
        if self.list_widget.count() != 0:
            self.list_widget.clear()
    # add items from tree_model to list_widget
        for item in self.tree_object.tree_list:
            list_item = qtw.QListWidgetItem()
            item_text = item['item_text']
            item_address = item['item_address']
            list_item.setText(item_text)
            list_item.setData(100, qtc.QVariant(item_address))
            self.list_widget.addItem(list_item)
            
    def on_item_click(self, item):
        print(item.data(100))

    def on_item_double_click(self, item):
        self.list_widget.itemChanged.disconnect(self.finish_editing_item)
        item.setFlags(item.flags() | qtc.Qt.ItemFlag.ItemIsEditable)
        self.list_widget.editItem(item)
        
        self.list_widget.itemChanged.connect(self.finish_editing_item)

    def finish_editing_item(self, item):
        item_address = item.data(100)
        new_text = item.text()
        old_text = self.tree_object.get_item(item_address)[1]
        if new_text != old_text:
            self.tree_object.rename_item(item_address, new_text)
            self.tree_object.make_tree_list()
            self.populate_list_widget()
    
    def insert_item(self):
        if not self.list_widget.selectedItems():
            return 'nothing selected'
        parent_item = self.list_widget.currentItem()
        parent_address = parent_item.data(100)
        current_row = self.list_widget.currentRow()
        if parent_address == 'root':
            parent_address = []
        new_item_address = parent_address.copy()
        new_item_address.append(0)
        new_item = qtw.QListWidgetItem()
        new_item.setData(100, qtc.QVariant(new_item_address))
        # add new row and select the item
        self.list_widget.insertItem(current_row + 1, new_item)
        
        # insert item into tree_object
        self.tree_object.insert_item(parent_address, '_')
        self.tree_object.make_tree_list()
        new_item.setSelected(True)
        self.on_item_double_click(new_item)
        
    def remove_node(self):
        if self.list_widget.selectedItems() == []:
            return print('nothing selected')      
        item = self.list_widget.currentItem()
        item_address = item.data(100)
        if item == 'root' or item == []:
            # removing root node not yet available
            return 'coming soon'
        # rm node
        self.tree_object.rm(item_address)
        self.tree_object.make_tree_list()
        self.populate_list_widget()
    
    def reposition_item(self):
        print(self.reposition_item_button_mode)
        if self.list_widget.selectedItems() == []:
            return print('nothing selected')  
               
        # check if initial button press
        if self.reposition_item_button_mode == 'initial_press':
            item = self.list_widget.currentItem()
            item_address = item.data(100)
            if item_address == 'root' or item == []:
                return print('cannot reposition root')
            self.reposition_item_address = item_address
            self.reposition_item_button_mode = 'final_press'
            
        
        elif self.reposition_item_button_mode == 'final_press':
            item = self.list_widget.currentItem()
            item_address = item.data(100)
            rank = item_address[-1]
            if item == 'root' or item == []:
                return print('cannot reposition root')
            self.tree_object.reposition_item(self.reposition_item_address, rank)
            self.tree_object.make_tree_list()
            self.populate_list_widget()
            self.reposition_item_button_mode = 'initial_press'
            self.reposition_item_address = None
            
    def reparent_node(self):
        if self.reparent_node_button_mode == 'initial_press':
            item = self.list_widget.currentItem()
            item_address = item.data(100)
            if item == 'root' or item == []:
                return print('cannot reparent root')
            self.reparent_node_address = item_address
            self.reparent_node_button_mode = 'final_press'
            
        
        elif self.reparent_node_button_mode == 'final_press':
            item = self.list_widget.currentItem()
            new_parent_address = item.data(100)
            if new_parent_address == 'root':
                new_parent_address = []
            self.tree_object.reparent(self.reparent_node_address, new_parent_address)
            self.tree_object.make_tree_list()
            self.populate_list_widget()
            self.reparent_node_button_mode = 'initial_press'
            self.reparent_node_address = None
            
    def save(self):
        self.tree_object.save(self.tree_file_str)
        
    def load(self):
        filename, _ = qtw.QFileDialog.getOpenFileName()
        self.tree_object.load(filename)
        self.tree_object.make_tree_list()
        self.populate_list_widget()        
        
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())