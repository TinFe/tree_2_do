import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


# create a MainWindow class
class ListModel(qtg.QStandardItemModel):
    def __init__(self):
        super().__init__()
        # Create some standard items to represent the to-do items
        item1 = qtg.QStandardItem('Research')
        item2 = qtg.QStandardItem('Projects')
        item3 = qtg.QStandardItem('Networking')

        item4 = qtg.QStandardItem('Data Structures')
        item5 = qtg.QStandardItem('To Do List')
        item6 = qtg.QStandardItem('Meetup')

        self.appendRow([item1, item2, item3])
        self.appendRow([item4, item5, item6])


