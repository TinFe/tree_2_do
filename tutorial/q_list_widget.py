import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


# create a MainWindow class
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_layout = qtw.QHBoxLayout()
        self.main_widget = qtw.QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)


        self.list_widget = qtw.QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setDragEnabled(True)

        items = ['complete pyqt6 tutorial', 'finish chapter problems', 'create C looping program']

        for item in items:
            list_item = qtw.QListWidgetItem()
            list_item.setText(item)
            self.list_widget.addItem(list_item)

        add_button = qtw.QPushButton('Add')
        add_button.clicked.connect(self.addListItem)

        insert_button = qtw.QPushButton('Insert')
        insert_button.clicked.connect(self.insertItemInList)

        remove_button = qtw.QPushButton('Remove')
        remove_button.clicked.connect(self.removeOneItem)

        clear_button = qtw.QPushButton('Clear')
        clear_button.clicked.connect(self.list_widget.clear)

        # layouts
        right_v_box = qtw.QVBoxLayout()
        right_v_box.addWidget(add_button)
        right_v_box.addWidget(insert_button)
        right_v_box.addWidget(remove_button)
        right_v_box.addWidget(clear_button)

        self.main_layout.addWidget(self.list_widget)
        self.main_layout.addLayout(right_v_box)

        self.show()

    def addListItem(self):
        text, ok = qtw.QInputDialog.getText(self, "New Item", "Add item:")
        if ok and text != "":
            list_item = qtw.QListWidgetItem()
            list_item.setText(text)
            self.list_widget.addItem(list_item)

    def insertItemInList(self):
        text, ok = qtw.QInputDialog.getText(self, "Insert Item:", "Insert Item:")
        if ok and text != "":
            row = self.list_widget.currentRow()
            row += 1
            new_item = qtw.QListWidgetItem()
            new_item.setText(text)
            self.list_widget.insertItem(row, new_item)

    def removeOneItem(self):
        row = self.list_widget.currentRow()
        item = self.list_widget.takeItem(row)
        del item

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
