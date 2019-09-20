from PyQt5.QtWidgets import *
import config

from detect import DetectC
from multiprocessing.pool import ThreadPool
from threading import Thread, Event
from PyQt5 import QtGui

CONFIG = {
    # PATH
    'iconPath': config.iconFilePath,
    # UI file
    'formClass': config.form_class,
    # Command line
    'command1': config.command_lines2,
    'command2': config.command_lines2,
    # Time Out
    'TimeROut': config.TimeR_out_sec,
    'TimeWOut': config.TimeW_out_sec,
    # Message
    'TimeOutMessage': config.Time_out_alert,
    'MessageWidth': config.msg_width,
    'MessageHeight': config.msg_height,
    # DetectPerCent
    'DetectPercent': config.detect_percent
}


class Window(QMainWindow, CONFIG['formClass']):
    def __init__(self):
        self.detectC = DetectC()
        self.name_dic = {}
        super().__init__()
        self.setupUi(self)
        self.Btt_WearingDetect.clicked.connect(self.btt_wearing_detect)
        self.Btt_Realtime_Detect.clicked.connect(self.btt_realtime_detect)

    def btt_wearing_detect(self):
        pool = ThreadPool(processes=1)
        watcher = pool.apply_async(self.detectC.start_detect,
                                   args=(CONFIG['command2'], CONFIG['TimeROut']),
                                   callback=self.process_callback)
        watcher.daemon = True
        pool.close()
        pool.join()
        print("Detect Closed..#######################################################################################")

        msg_str_wearing = ""
        msg_str_unwearing = ""
        num_all_feature = len(self.name_dic)
        num_wearing = 0
        print("####All Feature : " + str(num_all_feature) + " ####")
        for name in self.name_dic:
            if self.name_dic[name] == 1:
                msg_str_wearing += name + "\t"
                num_wearing += 1
            elif self.name_dic[name] == 0:
                msg_str_unwearing += name + "\t"
        msg_str_wearing += "\t착용중\n"
        msg_str_unwearing += "\t미착용\n"
        add_str_unwearing = "----------------------------------------------------------------------------------\n" \
                            "미착용 물품을 착용하고 다시 시도 하세요."
        print("####Detect Feature : " + str(num_wearing) + " ####")
        wearingPercent = num_wearing/num_all_feature * 100
        print("####Detect Percent : " + str(wearingPercent) + "% ####")
        print("####System Detection Thresh : " + str(CONFIG['DetectPercent']) + "% ####")
        print_msg = ""
        if wearingPercent < float(CONFIG['DetectPercent']):
            print_msg += msg_str_wearing + msg_str_unwearing + add_str_unwearing
        else:
            print_msg = "#####모든 안전장비가 갖춰졌습니다.#####\n#####작업을 시작하세요!!!#####"
        msg = self.make_qmessagebox("####결과####", print_msg, QMessageBox.Ok)
        # done = Event()
        # waitmessagebox = Thread(target=self.exit_messagebox, args=(msg, done, CONFIG['TimeOutMessage']))
        # waitmessagebox.daemon = True
        # waitmessagebox.start()
        result = msg.exec_()
        # done.set()
        print("EndDetect")
        """
        if result == QMessageBox.Ok:
            print("end")
        """

    def btt_realtime_detect(self):
        pool = ThreadPool(processes=1)
        watcher = pool.apply_async(self.detectC.start_detect,
                                   args=(CONFIG['command2'], CONFIG['TimeROut']),
                                   callback=self.process_callback)
        watcher.daemon = True
        pool.close()
        pool.join()
        print("Detect Closed..#######################################################################################")

        for name in self.name_dic:
            if self.name_dic[name] == 1:
                print(name + " : " + "있음")
            elif self.name_dic[name] == 0:
                print(name + " : " + "없음")

        msg = self.make_qmessagebox("경고", "알람", QMessageBox.Ok)
        done = Event()
        waitmessagebox = Thread(target=self.exit_messagebox, args=(msg, done, CONFIG['TimeOutMessage']))
        waitmessagebox.daemon = True
        waitmessagebox.start()
        result = msg.exec_()
        done.set()
        print("EndDetect")
        """
        if result == QMessageBox.Ok:
            print("end")
        """

    def process_callback(self, result):
        self.name_dic = result

    def make_qmessagebox(self, title, text, button):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(button)
        msg.setFixedHeight(CONFIG['MessageHeight'])
        msg.setFixedWidth(CONFIG['MessageWidth'])
        msg.setWindowIcon(QtGui.QIcon(CONFIG['iconPath']+"/icon1.jpg"))
        return msg

    def exit_messagebox(self, messagebox, done, timeout):
        if not done.wait(timeout):
            messagebox.close()
