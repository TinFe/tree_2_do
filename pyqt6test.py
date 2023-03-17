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
        
        self.list_widget = qtw.QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        
        # add items from tree_model to list_widget
        for item in l:
            list_item = qtw.QListWidgetItem()
            list_item.setText(item['item_text'])
            self.list_widget.addItem(list_item)
        
        main_widget.layout().addWidget(self.list_widget)
        
        


        
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())