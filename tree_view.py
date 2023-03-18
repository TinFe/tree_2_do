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
        
        self.control_panel = qtw.QWidget()
        self.control_panel.setLayout(qtw.QHBoxLayout())
        self.insert_item_button = qtw.QPushButton('+')
        self.insert_item_button.clicked.connect(self.insert_item)
        self.control_panel.layout().addWidget(self.insert_item_button)
        
        self.tree_object = ListTree('_')
        self.tree_object.load('test.json')
        self.tree_object.make_tree_list()
        
        self.list_widget = qtw.QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemClicked.connect(self.on_item_click)
        self.list_widget.setDragEnabled(True)
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_click)
        self.list_widget.itemChanged.connect(self.finish_editing_item)
        
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
        
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())