import sys
import time
import datetime
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

        #init & configure
        # mycomport=serial.Serial()
        self.mycomport.port="COM4"
        self.mycomport.baudrate=9600

        self.LAB_error.setStyleSheet("color:red;")
        self.LAB_comrxbuf.setStyleSheet("background-color:white;")

        self.start_time = self.end_time = time.time()

        self.PBTNT.clicked.connect(self.myTest1)
        self.PBTNT_2.clicked.connect(self.myTest2)
        self.PBTNT_pause.clicked.connect(self.myTest3)
        self.PBTNT_comtx.clicked.connect(self.myUartTX)

    def myTest1(self):
    #serial test - force open com port
        try:
            self.mycomport.close()
            self.mycomport.open()
            if self.mycomport.isOpen() :
                print("Port was Opened")
                #change state
                self.PBTNT.setChecked(True) 
                self.flab_error("","clear")
                # self.LAB_error.clear()
                #invoke RX
                self.myUartCtrl("RX")
        except SerialException as e:
                print("Port Open Failed- No such COM port")
                print(e)
                self.flab_error(str(e),"show")
                # self.LAB_error.setText(str(e))
                self.PBTNT.setChecked(False) 
        # else:
        #     print("Port is close and opening")

        # print(self.PBTNT.isChecked())
        # self.showStatus("hello" )
    def myTest2(self):
    #thread test with QThread
        self.thread4=MyThread(4, 200) # label, delay
        self.thread4.callback.connect(self.drawUi)
        self.thread4.start() 

           
    def myTest3(self):
        # self.thread4.runFlag=False #quit thread
        try:
            self.thread4.passFlag= ~self.thread4.passFlag
        except:
            print("No thread Created") 
        # self.thread4.passFlag=True
    def myUartTX(self):
        if self.mycomport.isOpen():
            print("here")
            self.myUartCtrl("TX")
        else:
            print("port not open")
    def myUartRX(self):
        # if self.mycomport.isOpen() :
        # while True:
        #     time.sleep(0.01)
            while self.mycomport.in_waiting:
                data_raw=self.mycomport.readline()
                data=data_raw.decode()
                print('receive raw data :',data_raw)
                print('decode data :',data)

    def myUartCtrl(self,myCMD):
        if myCMD=="init":
            self.showStatus("Uart init")
        elif myCMD=="TX":
            self.showStatus("Uart Transmit")
            cmdstr=self.LSTW_atcmds.currentItem().text()+ "\r\n"
            vbytearray=bytearray(cmdstr.encode())
            self.mycomport.write(vbytearray) #default b'AT\r\n'
            self.flab_dmsg('TX OK - %s' %cmdstr,1)#print
            # print(vbytearray)
        else:#RX
            self.showStatus("Uart else event(RX)")
            self.thread2=MyThread(2, 10) # label, delay
            self.thread2.callback.connect(self.myUartRX)
            self.thread2.start() 

    def drawUi(self,index,label):
        if label==4:
            self.showTimer()
        else:
            print("Thread invoke failed")
          
    def showTimer(self):
        self.end_time=time.time()
        self.LAB_runtime.setText(str(self.end_time-self.start_time))
        self.LAB_datetime.setText(str(datetime.datetime.now()))
        self.LAB_showflag.setText(str(self.thread4.passFlag))
        self.LAB_showcount.setText(str(self.thread4.count))
    def showStatus(self, mystr):
        
        mytick = str(time.time())
        # self.LAB_dmsg.setText(mystr +"- " + mytick + "\r\n"  + mypreTxt )#+ mytick)
        self.flab_dmsg(mystr, 1)

    def flab_dmsg(self,pstr,cmd): #handle Label_dmsg
        mypreTxt= self.LAB_dmsg.text()
        if cmd==1:
            self.LAB_dmsg.setText(pstr+"\r\n"+mypreTxt)
        else:
            self.flab_error("lab_dmsg", "")

    def flab_error(self,pstr,cmd): #handle Label_error
        if cmd=="clear":
            self.LAB_error.clear()
        elif cmd=="show":
            self.LAB_error.setText(pstr)
        else:
            self.LAB_error.setText("Abnormal -" + pstr)
    def printmsg(self,pstr):
        print(pstr)

if __name__ == "__main__":

    app = QApplication(sys.argv) #import sys
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())