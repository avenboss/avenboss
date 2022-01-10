from PyQt5.QtCore import QThread, pyqtSignal

class MyThread(QThread):
    callback = pyqtSignal(int, int)#自定義訊號, Qt的文件中有說明, 必需為類別變數
    def __init__(self, label, delay, parent=None):#初始化參數
        super().__init__(parent)

        self.runFlag = True #for while loop terminate
        self.passFlag= False #skip counting in while loop
        self.label=label
        self.delay=delay
        
    def __del__(self):
        self.runFlag = False
        self.wait()

    def run(self):
        print("thread run " + str(self.label))
        while_index=0
        while self.runFlag:
            self.callback.emit(while_index, self.label) #傳遞參數(整數1，整數2)
            if self.label==3 :
            #     print(threading.currentThread().getName() + " / " + str(index)) #import threading
                if self.passFlag :
                    continue
            self.msleep(self.delay)
            while_index+=1
#       print(threading.currentThread().getName() + " / End : " + str(index)) #import threading
        print("thread quit " + str(self.label))
        self.quit()
        self.wait()