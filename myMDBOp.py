import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from pymongo import MongoClient
from PyQt5 import QtCore

#include UI file which has 'pyuic5' from ui file developed by QT Designer
from myMDB import Ui_MainWindow

client = MongoClient('localhost',27017)
#client = MongoClient('mongodb://localhost:27017/')

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #add initial procedure
        self.PBTN.clicked.connect(self.pushBTN_click)
        # self.LAB_dmsg.text="hello"

    def showStatus(self,dmsglevel, txtbody):
        if dmsglevel==1:
            # msg=self.LAB_dmsg.text()
            print(txtbody)
            self.LAB_dmsg.setText(self.LAB_dmsg.text() + txtbody)
            print(self.LAB_dmsg.text() + txtbody)
        # else:
            print("showStatus-"+txtbody)
    def DBfind(self):
        dblist = client.list_database_names()

        mydb=client["ST50X"]
        collist=mydb.list_collection_names()
        
        mycol= mydb["AI50H"]
        if "ST50X" in dblist:
            print("database exist ! " )
            print (len(collist))
            
            if (self.CBOX_db.findText("ST50X")== -1):
                self.CBOX_db.addItem("ST50X")
            if "ST50H" in collist:
                print('collections - %s %s %s %s' %(collist[0] ,collist[1],collist[2],collist[3]))
                if (len(collist)>0):
                    for x in range(len(collist)):
                        print(collist[x])
                        # if self.LSTW_collection.findItems(collist[x],QtCore.Qt.MatchFlag.MatchFixedString):
                        #     # print("重複Item")
                        #     self.LSTW_collection.addItem(collist[x])
                        # else:
                        #     print('重複Item %s add' %(collist[x]))
        else:
            print("DB 不存在")
         #collect = db.
    def pushBTN_click(self):   
        print("push button press here")
        self.showStatus(1,"call showStatus")
        # self.LAB_dmsg.setText("hello")

if __name__ == "__main__":

    app = QApplication(sys.argv) #import sys
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())