import subprocess
from threading import Thread, Event
import os


rootPath = os.getcwd()
darknetPath = rootPath+"/darknet"
command_lines1 = './darknet.exe detector test cfg/coco.data yolov3.cfg yolov3.weights -ext_output dog.jpg'


def kill_on_timeout(done, timeout, proc):
    if not done.wait(timeout):
        proc.kill()


def exec_command(command, timeout):
    os.chdir(darknetPath)
    done = Event()
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    watcher = Thread(target=kill_on_timeout, args=(done, timeout, proc))
    watcher.daemon = True
    watcher.start()

    data, stderr = proc.communicate()
    done.set()
    os.chdir(rootPath)
    return data, stderr, proc.returncode


def main():
    print(exec_command(command_lines1, 10))


if __name__ == "__main__":
    main()
