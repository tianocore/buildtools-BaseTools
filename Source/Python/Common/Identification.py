# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

"""
This file is used to define the identification of INF/DEC/DSC files
"""

class Identification(object):
  def __init__(self):
    self.FileName = ''
    self.FileFullPath = ''
    self.FileRelativePath = ''

  def GetFileName(self, FileFullPath, FileRelativePath):
    pass

  def GetFileFullPath(self, FileName, FileRelativePath):
    pass

  def GetFileRelativePath(self, FileName, FileFullPath):
    pass

if __name__ == '__main__':
  id = Identification()
