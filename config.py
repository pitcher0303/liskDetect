# Config.py
import os
from PyQt5 import uic

# Command
command_lines1 = './darknet.exe detector test cfg/coco.data yolov3.cfg yolov3.weights -ext_output dog.jpg'
command_lines2 = './darknet.exe detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights -c 0'
command_lines3 = './darknet.exe detector demo LINC/obj.data LINC/yolo-obj.cfg LINC/yolo-obj_16000.weights -c 0'

# Executable Program
powershell = "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
cmd = "C:/Windows/System32/cmd.exe"

# PATH
rootPath = os.getcwd()
darknetPath = rootPath+"/darknet"
nameFilePath = rootPath+"/data/coco.names"
iconFilePath = rootPath+"/IconFile"

# UI file
form_class = uic.loadUiType("mainView.ui")[0]

# Time_out_sec
TimeW_out_sec = 10
TimeR_out_sec = 40
Time_out_alert = 10

# Queue Time out value, Time to print Queue
queue_time_out = 0.1

# Name Dictionary
name_dic = {}
f = open(nameFilePath, 'r')
lines = f.read()
for line in lines.split('\n'):
    name_dic[line] = 0

# Message Box Width, Height
msg_width = 800
msg_height = 600

# Detect Percent
detect_percent = 0
