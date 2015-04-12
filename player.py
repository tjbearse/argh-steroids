import subprocess
from Queue import Queue, Empty
import sys
from threading import Thread

# credit to http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
# for reference

# on posix system?
ON_POSIX = 'posix' in sys.builtin_module_names

class PlayerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def enqueue_output(out, queue):
    try:
        for line in iter(out.readline, b''):
            queue.put(line)
    finally:
        out.close()

class Player(object):
    def __init__(self, invoke_str):
        try:
            self._proc = subprocess.Popen(invoke_str.split(),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    #bufsize=1,
                    #close_fds=ON_POSIX
                )
        except OSError:
            raise PlayerError("Failed to start %s" % invoke_str)
        self._queue = Queue()
        self._thread = Thread(target=enqueue_output, args=(self._proc.stdout, self._queue))
        self._thread.daemon = True # thread dies with program
        self._thread.start()

    def __del__(self):
        self._proc.kill()

    # throws Empty on empty
    def read_nowait(self):
        return self._queue.get_nowait()

    def read_timeout(self, timeout):
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            raise PlayerError("Read timeout")

    def write(self, string):
        try:
            self._proc.stdin.write("%s\n" % string)
            self._proc.stdin.flush()
        except IOError, OSError:
            raise PlayerError("Failed write")
