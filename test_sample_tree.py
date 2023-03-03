import sys
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


# create a MainWindow class
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = qtw.QWidget()
        self.main_layout = qtw.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.tree_widget = qtw.QTreeWidget()
        self.tree_widget.setColumnCount(1)
        self.tree_widget.setHeaderLabel("Fruit Type")
        self.tree_widget.setColumnWidth(0, 160)

        category_1 = qtw.QTreeWidgetItem(self.tree_widget, "Apples")

        apple_list =['Braeburn',"Ginger Gold", "Green-yellow", "icons/ginger_gold.png"]
        for i in range(len(apple_list)):
            category_1_child = qtw.QTreeWidgetItem(apple_list[i])
            category_1.addChild(category_1_child)
        category_2 = qtw.QTreeWidgetItem(self.tree_widget,
                                     ["Oranges", "A type of citrus fruit"])
        orange_list = [
            ["Navel", "Sweet and slightly bitter",
             "icons/navel.png"],
            ["Blood Orange", "Juicy and tart",
             "icons/blood_orange.png"],
            ["Clementine", "Usually seedless",
             "icons/clementine.png"]]

        for i in range(len(apple_list)):
            category_2_child = qtw.QTreeWidgetItem(
                orange_list[i][:2])
            category_2.addChild(category_2_child)

        self.main_layout.addWidget(self.tree_widget)

        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
