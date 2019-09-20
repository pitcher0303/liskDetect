import sys
import time
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue, Empty

ON_POSIX = 'posix' in sys.builtin_module_names


################################################################################
def enqueue_stdout(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


################################################################################
def enqueue_stderr(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


################################################################################
def do():
    po = Popen([sys.executable, 'po_callee.py'],
              stdout=PIPE, stderr=PIPE,
              bufsize=1, close_fds=ON_POSIX)
    q_out, q_err = Queue(), Queue()
    t_out = Thread(target=enqueue_stdout, args=(po.stdout, q_out))
    t_out.daemon = True  # thread dies with the program
    t_out.start()
    t_err = Thread(target=enqueue_stderr, args=(po.stderr, q_err))
    t_err.daemon = True  # thread dies with the program
    t_err.start()

    while po.poll() is None:
        try:
            line = q_out.get_nowait()
            if line:
                print(line.decode('utf-8').rstrip())
        except Empty:
            pass
        try:
            line = q_err.get_nowait()  # or q.get(timeout=.1)
            if line:
                sys.stderr.write('%s\n' % line.decode('utf-8').rstrip())
        except Empty:
            pass
        time.sleep(1)


################################################################################
if __name__ == '__main__':
    do()
