import sys
import re


class Entity():
    regex = re.compile(r"""(?P<type> [a-z]+ )
            \( (?P<x> \d+(\.\d+)? ) ,\  (?P<y>) \d+(\.\d+)? \)
            \( (?P<dx> \d+(\.\d+)? ) ,\ (?P<dy> \d+(\.\d+)? ) \)
            (?P<scale> \d+(\.\d+)? )""", re.VERBOSE)
    def __init__(self, string):
       m = regex.match(string)
       self.type = m.group("type")
       self.x = float(m.group("x"))
       self.y = float(m.group("y"))
       self.dx = float(m.group("dx"))
       self.dy = float(m.group("dy"))
       self.scale = float(m.group("scale"))

class State():
    def __init__(self, fd):
        num = int(fd.readline())
        self.entities = []
        for i in range(num):
            self.entities = Entity(fd.readline())
        fd.readline() # "stop"


class Response():
    def __init__(self):
        self._cw = False
        self._thrust = False
        self._fire = False
    def set_cw(self):
        self._cw = True
    def set_ccw(self):
        self._cw = False
    def set_thrust(self, on):
        self._thrust = on
    def set_fire(self, on):
        self._fire = on
    def send(self):
        turn = "cw" if self._cw else "ccw"
        thrust = "on" if self._thrust else "off"
        fire = "on" if self._fire else "off"
        sys.stdout.write("%s %s %s\n" % (turn, thrust, fire))
        sys.stdout.flush()

        
    
#turn, thrust, fire
while True:
    read = sys.stdin.readline()
    #print >>sys.stderr, read
    r = Response()
    r.set_fire(True)
    r.set_thrust(True)
    r.set_cw()
    r.send()
