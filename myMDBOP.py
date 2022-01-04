import sys


from PyQt5.QtWidgets import QApplication, QMainWindow

from myMDB import Ui_MainWindow



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":

    app = QApplication(sys.argv) #import sys
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())