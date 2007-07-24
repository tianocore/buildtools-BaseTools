import os
from threading import *
from subprocess import *



class BuildSpawn(Thread):
    def __init__(self, Sem=None, Filename=None, Args=None, Num=0):
        Thread.__init__(self)
        self.sem=Sem
        self.filename=Filename
        self.args=Args
        self.num=Num
        

    def run(self):
        self.sem.acquire()
        p = Popen(["nmake", "/nologo", "-f", self.filename, self.args], env=os.environ, cwd=os.path.dirname(self.filename))
        p.communicate()
        if p.returncode != 0:
            return p.returncode
        self.sem.release()