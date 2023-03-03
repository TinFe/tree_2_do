import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


# create a MainWindow class
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = qtw.QWidget()
        # self.main_layout = qtw.Q BoxLayout()
        # self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)



        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
