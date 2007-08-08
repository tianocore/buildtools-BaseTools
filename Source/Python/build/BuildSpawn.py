#
#  Copyright (c) 2007, Intel Corporation
#
#  All rights reserved. This program and the accompanying materials
#  are licensed and made available under the terms and conditions of the BSD License
#  which accompanies this distribution.  The full text of the license may be found at
#  http://opensource.org/licenses/bsd-license.php
#
#  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
#  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#


import os
from threading import *
from subprocess import *

import Common.EdkLogger as EdkLogger


class BuildSpawn(Thread):
    def __init__(self, ReturnCode, Sem=None, Filename=None, Args=None, Num=0):
        Thread.__init__(self)
        self.sem=Sem
        self.filename=Filename
        self.args=Args
        self.num=Num
        self.returncode=ReturnCode
        

    def run(self):
        self.sem.acquire()
        p = Popen(["nmake", "/nologo", "-f", self.filename, self.args], stdout=PIPE, stderr=PIPE, env=os.environ, cwd=os.path.dirname(self.filename))
        while p.poll() == None:
            EdkLogger.info(p.stdout.readline()[:-2])
        EdkLogger.info(p.stdout.read())
        if p.returncode != 0:
            self.returncode[0] = 1
            EdkLogger.quiet(p.stderr.read())
        self.sem.release()
