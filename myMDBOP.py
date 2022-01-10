import sys
import time
import serial

from PyQt5.QtWidgets import QApplication, QMainWindow
from serial import SerialException



# QT GUI 
from myMDB import Ui_MainWindow
from myThred import MyThread


class MainWindow(QMainWindow, Ui_MainWindow):
    mycomport=serial.Serial()
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # mycomport=serial.Serial()
        self.mycomport.port="COM4"
        self.mycomport.baudrate=9600

        self.PBTNT.clicked.connect(self.myTest1)
        self.PBTNT_2.clicked.connect(self.myTest2)

    def myTest1(self):
        #force open com port
        try:
            self.mycomport.close()
            self.mycomport.open()
            if self.mycomport.isOpen() :
                print("Port was Opened")
                self.PBTNT.setChecked(True) 
        except SerialException:
                print("Port Open Failed- No such COM port")
                self.PBTNT.setChecked(False) 
        # else:
        #     print("Port is close and opening")

        # print(self.PBTNT.isChecked())
        # self.showStatus("hello" )
    def myTest2(self):
        self.thread4=MyThread(4, 200)
        self.thread4.callback.connect(self.drawUi)
        self.thread4.start()    
          
    def myUartCtrl(self,myCMD):
        if myCMD=="init":
            showStatus("Uart init")
        elif myCMD=="TX":
            showStatus("Uart Transmit")
        else:
            showStatus("Uart else event")
          


    def showStatus(self, mystr):
        mypreTxt= self.LAB_dmsg.text()
        mytick = str(time.time())
        self.LAB_dmsg.setText(mystr +"- " + mytick + "\r\n"  + mypreTxt )#+ mytick)


if __name__ == "__main__":

    app = QApplication(sys.argv) #import sys
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())