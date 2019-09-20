import subprocess as sb
import os
import sys

from threading import Thread, Event
from PyQt5.QtWidgets import *
from PyQt5 import uic

command_lines1 = './darknet.exe detector test cfg/coco.data yolov3.cfg yolov3.weights -ext_output dog.jpg'
command_lines2 = './darknet.exe detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights -c 0'
command_lines3 = './darknet.exe detector demo LINC/obj.data LINC/yolo-obj.cfg LINC/yolo-obj_8900.weights -c 0'
powershell = "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
cmd = "C:/Windows/System32/cmd.exe"
rootPath = os.getcwd()
darknetPath = rootPath+"/darknet"
# UI file
form_class = uic.loadUiType("mainView.ui")[0]

# Time_out_sec
TimeW_out_sec = 10
TimeR_out_sec = 30


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Btt_WearingDetect.clicked.connect(self.btt_wearing_detect)
        self.Btt_Realtime_Detect.clicked.connect(self.btt_realtime_detect)

    def btt_wearing_detect(self):
        detect_demon = Thread(target=start_detect, args=(command_lines1, TimeW_out_sec))
        detect_demon.daemon = True
        detect_demon.start()
        # print(start_detect(command_lines1, TimeW_out_sec))

    def btt_realtime_detect(self):
        detect_demon = Thread(target=start_detect, args=(command_lines2, TimeR_out_sec))
        detect_demon.daemon = True
        detect_demon.start()
        # print(start_detect(command_lines2, TimeR_out_sec))


def start_detect(command, timeout):
    os.chdir(darknetPath)

    # popen = sb.Popen(['dir'], shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
    # (stdoutdata, stderrdata) = popen.communicate()
    # print(stdoutdata.decode('ms949').splitlines())
    done = Event()
    popen = sb.Popen(command, stdout=sb.PIPE, stderr=sb.PIPE)
    print("startTimer")
    watcher = Thread(target=kill_on_timeout, args=(done, timeout, popen))
    watcher.daemon = True
    watcher.start()
    stdoutdata, stderrdata = popen.communicate()
    done.set()
    print("endTimer")
    os.chdir(rootPath)

    return stdoutdata.decode('ms949').splitlines(), stderrdata.decode('ms949').splitlines()


def kill_on_timeout(done, timeout, popen):
    if not done.wait(timeout):
        popen.kill()


def main():
    print(start_detect(command_lines1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
