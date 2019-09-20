import sys

from MyWindow import Window
from PyQt5.QtWidgets import *
from PyQt5 import uic

# UI file
form_class = uic.loadUiType("mainView.ui")[0]

# Time_out_sec
TimeW_out_sec = 10
TimeR_out_sec = 60

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Window()
    myWindow.show()
    app.exec_()
