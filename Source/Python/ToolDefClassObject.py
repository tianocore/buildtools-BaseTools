# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define each component of tools_def.txt file
#

import EdkLogger
from Dictionary import *

class ToolDefClassObject(object):
  def __init__(self, filename = None):
    self.ToolsDefTxtDictionary = {}
    
    self.ToolsDefTxtDatabase = {
      TAB_TOD_DEFINES_TARGET                       : [],
      TAB_TOD_DEFINES_TOOL_CHAIN_TAG               : [],
      TAB_TOD_DEFINES_TARGET_ARCH                  : [],
      TAB_TOD_DEFINES_COMMAND_TYPE                 : []
    }
    if filename != None:
      self.LoadToolDefFile(filename)

  def LoadToolDefFile(self, filename):
    EdkLogger.info('LoadToolDefFile() Start')
    if filename != None:
      ConvertTextFileToDictionary(filename, self.ToolsDefTxtDictionary, '#', '=', False, None)

    self.ToolsDefTxtDatabase = {
      TAB_TOD_DEFINES_TARGET                       : [],
      TAB_TOD_DEFINES_TOOL_CHAIN_TAG               : [],
      TAB_TOD_DEFINES_TARGET_ARCH                  : [],
      TAB_TOD_DEFINES_COMMAND_TYPE                 : []
    }

    for Key in dict(self.ToolsDefTxtDictionary):
      List = Key.split('_')
      if len(List) != 5:
        del self.ToolsDefTxtDictionary[Key]
      elif List[4] == '*':
        del self.ToolsDefTxtDictionary[Key]
      else:
        if List[0] != '*':
          self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET] += [List[0]]
        if List[1] != '*':
          self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG] += [List[1]]
        if List[2] != '*':
          self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH] += [List[2]]
        if List[3] != '*':
          self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE] += [List[3]]
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET]         = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET]))
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG] = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG]))
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH]    = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH]))
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE]   = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE]))
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET].sort()
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG].sort()
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH].sort()
    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE].sort()

    KeyList = [TAB_TOD_DEFINES_TARGET, TAB_TOD_DEFINES_TOOL_CHAIN_TAG, TAB_TOD_DEFINES_TARGET_ARCH, TAB_TOD_DEFINES_COMMAND_TYPE]
    for Index in range(3,-1,-1):
      for Key in dict(self.ToolsDefTxtDictionary):
        List = Key.split('_')
        if List[Index] == '*':
          for String in self.ToolsDefTxtDatabase[KeyList[Index]]:
            List[Index] = String
            NewKey = '%s_%s_%s_%s_%s' % tuple(List)
            if NewKey not in self.ToolsDefTxtDictionary:
              self.ToolsDefTxtDictionary[NewKey] = self.ToolsDefTxtDictionary[Key]
            continue
          del self.ToolsDefTxtDictionary[Key]
        elif List[Index] not in self.ToolsDefTxtDatabase[KeyList[Index]]:
          del self.ToolsDefTxtDictionary[Key]
    
    EdkLogger.info('LoadToolDefFile() End')
    
if __name__ == '__main__':
  td = ToolDefClassObject('tool_def.txt')
  print td.ToolsDefTxtDatabase