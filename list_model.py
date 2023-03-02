import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


# create a MainWindow class
class ListModel(qtg.QStandardItemModel):
    def __init__(self):
        super().__init__()
        # Create some standard items to represent the to-do items
        item1 = qtg.QStandardItem('Do something')
        self.appendRow([item1, qtg.QStandardItem('Not started')])


