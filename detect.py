import os
import sys
import time
import subprocess as sb
from threading import Thread, Event
from queue import Queue, Empty

import config
from multiprocessing.pool import ThreadPool

CONFIG = {
    # PATH
    'rootPath': config.rootPath,
    'darknetPath': config.darknetPath,
    'nameFilePath': config.nameFilePath,
    # nameFile to DIC
    'nameDic': config.name_dic,
    # Time_out_Queue
    'queueTimeOut': config.queue_time_out
}


def enqueue_stdout(out, queue):
    try:
        for line in iter(out.readline, b''):
            queue.put(line)
    except:
        pass
    out.close()


def enqueue_stderr(out, queue):
    try:
        for line in iter(out.readline, b''):
            queue.put(line)
    except:
        pass
    out.close()


def kill_on_timeout(done, timeout, popen):
    if not done.wait(timeout):
        popen.kill()
        print("endTimer")


class DetectC:

    def __init__(self):
        self.outline = ""
        super(DetectC, self).__init__()

    def start_detect(self, command, timeout):
        name_dic = CONFIG['nameDic']
        print(name_dic)
        os.chdir(CONFIG['darknetPath'])
        pool = ThreadPool(processes=1)

        done = Event()
        print("StartTimeout")
        popen = sb.Popen(command, stdout=sb.PIPE, stderr=sb.PIPE)
        q_out, q_err = Queue(), Queue()
        watcher = pool.apply_async(self.watchdetect, (popen, q_out, q_err), callback=self.watchdetect_callback)
        watcher.daemon = True

        t_out = Thread(target=enqueue_stdout, args=(popen.stdout, q_out))
        t_out.daemon = True  # thread dies with the program
        t_out.start()

        if not done.wait(timeout):
            popen.kill()

        pool.close()
        pool.join()

        result_list = self.outline.split(',')
        print(result_list)
        num = 0.0
        for result in result_list:
            resultP = result.split(':')
            if len(resultP) == 2:
                if resultP[0] in name_dic:
                    name_dic[resultP[0]] = 1
                    num += 1
        print("name dic")
        print(name_dic)
        print("EndTimeout")

        done.set()
        os.chdir(CONFIG['rootPath'])
        return name_dic

    def watchdetect(self, popen, q_out, q_err):
        result = ""
        while popen.poll() is None:
            try:
                line = q_out.get_nowait()
                datastr = ""
                if line:
                    datastr = line.decode('utf-8').rstrip()
                    # print(datastr)
                if datastr.startswith('DS,'):
                    result = datastr
            except Empty:
                pass
            try:
                line = q_err.get_nowait()  # or q.get(timeout=.1)
                if line:
                    sys.stderr.write('%s\n' % line.decode('utf-8').rstrip())
            except Empty:
                pass
            time.sleep(CONFIG['queueTimeOut'])
        return result

    def watchdetect_callback(self, result):
        self.outline = result

    def endstrdetect(self, popen, stdoutdata, stderrdata):
        stdoutdata, stderrdata = popen.communicate()
        print(stdoutdata, stderrdata)

        # outline = ""
        # popen = sb.Popen(['dir'], shell=True, stdout=sb.PIPE, stderr=sb.PIPE)
        # (stdoutdata, stderrdata) = popen.communicate()
        # print(stdoutdata.decode('ms949').splitlines())

        # watcher = Thread(target=self.kill_on_timeout, args=(done, timeout, popen))
        # watcher.daemon = True
        # watcher.start()

        # watcher = Thread(target=self.watchdetect, args=(popen, q_out, q_err))

        # t_err = Thread(target=enqueue_stderr, args=(popen.stderr, q_err))
        # t_err.daemon = True  # thread dies with the program
        # t_err.start()
        # endstrdetect = Thread(target=self.endstrdetect, args=(popen, outdata, outerr))
        # endstrdetect.start()
