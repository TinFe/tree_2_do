import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from list_model import ListModel

# create a MainWindow class
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree_view = qtw.QTreeView()
        self.tree_view.setModel(ListModel())

        self.setCentralWidget(self.tree_view)



        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
