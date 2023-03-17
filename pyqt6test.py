import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc
from tree_model import ListTree, s

# create a MainWindow class
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = qtw.QWidget()
        main_widget.setLayout(qtw.QVBoxLayout())
        self.setCentralWidget(main_widget)
        
        test_label = qtw.QLabel(s)
        main_widget.layout().addWidget(test_label)


        
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())