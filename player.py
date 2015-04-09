import subprocess
from Queue import Queue, Empty
import sys
from threading import Thread

# credit to http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
# for reference

# on posix system?
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

class Player(object):
    def __init__(self, invoke_str):
        self._proc = subprocess.Popen(invoke_str.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                #bufsize=1,
                #close_fds=ON_POSIX
            )
        self._queue = Queue()
        self._thread = Thread(target=enqueue_output, args=(self._proc.stdout, self._queue))
        self._thread.daemon = True # thread dies with program
        self._thread.start()
        #TODO supply world global settings

    # throws Empty on empty
    def read_nowait(self):
        return self._queue.get_nowait()

    def read_timeout(self, timeout):
        return self._queue.get(timeout=timeout)

    def write(self, string):
        self._proc.stdin.write("%s\n" % string)
        self._proc.stdin.flush()
