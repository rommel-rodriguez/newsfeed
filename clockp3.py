from PyQt5 import QtCore, QtWidgets
from time import strftime
class Main(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        #super(Main,self).__init__()
        self.initUI()
    def initUI(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.display(strftime("%H"+":"+"%M"))

        #self.setCentralWidget(self.lcd)
        #self.myVLayout = QtGui.QVBoxLayout(self)
        #self.myVLayout.addWidget(self.lcd)
        #self.setLayout(self.myVLayout)
        self.lcd.setGeometry(0,0,400,100)
        self.myCalendar = QtWidgets.QCalendarWidget(self)
        self.myCalendar.setGeometry(0,100,400,200)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.myCalendar.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.myCalendar.setAttribute(QtCore.Qt.WA_TranslucentBackground)

#--------------Window settings------------------
        self.setGeometry(300,300,400,100)
        self.setMinimumSize(400,300)
        self.setMaximumSize(400,300)
        self.setEnabled(False)
        self.setWindowTitle("Shadow's clock")

#--------------Slots ---------------------------

    def Time(self):
        self.lcd.display(strftime("%H"+":"+"%M"))

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



