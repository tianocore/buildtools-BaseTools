# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define each component of DEC file
#

import os
from String import *
from DataType import *
from Identification import *
from Dictionary import *

class DecObject(object):
  def __init__(self):
    object.__init__()

class DecDefines(DecObject):
  def __init__(self):
    self.DefinesDictionary = {
      #Req
      TAB_DEC_DEFINES_DEC_SPECIFICATION   : '',
      TAB_DEC_DEFINES_PACKAGE_NAME        : '',
      TAB_DEC_DEFINES_PACKAGE_GUID        : '',
      TAB_DEC_DEFINES_PACKAGE_VERSION     : ''
    }
    
class DecContents(DecObject):
  def __init__(self):
    self.Includes = []
    self.Guids = []
    self.Protocols = []
    self.Ppis = []
    self.LibraryClasses = []
    self.PcdsFixedAtBuild = []
    self.PcdsPatchableInModule = []
    self.PcdsFeatureFlag = []
    self.PcdsDynamic = []
    self.PcdsDynamicEx = []

class Dec(DecObject):
  def __init__(self, filename = None, isMergeAllArches = False):
    self.identification = Identification()
    self.Defines = DecDefines()
    
    self.Contents = {}
    for key in DataType.ARCH_LIST_FULL:
      self.Contents[key] = DecContents()
    
    self.KeyList = [
      TAB_INCLUDES, TAB_GUIDS, TAB_PROTOCOLS, TAB_PPIS, TAB_LIBRARY_CLASSES, \
      TAB_PCDS_FIXED_AT_BUILD_NULL, TAB_PCDS_PATCHABLE_IN_MODULE_NULL, TAB_PCDS_FEATURE_FLAG_NULL, \
      TAB_PCDS_DYNAMIC_NULL, TAB_PCDS_DYNAMIC_EX_NULL
    ]
  
    if filename != None:
      self.LoadDecFile(filename)
      
    if isMergeAllArches:
      self.MergeAllArches()      
  
  def ParseDec(self, Lines, Key, KeyField):
    GetMultipleValuesOfKeyFromLines(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
      
  def MergeAllArches(self):
    for key in self.KeyList:
      for arch in DataType.ARCH_LIST:
        Command = "self.Contents[arch]." + key + ".extend(" + "self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ")"
        eval(Command)

  def LoadDecFile(self, filename):
    f = open(filename, 'r').read()
    sects = f.split('[')
    for sect in sects:
      tab = (sect.split(TAB_SECTION_END, 1)[0]).upper()
      if tab == TAB_INF_DEFINES.upper():
        GetSingleValueOfKeyFromLines(sect, self.Defines.DefinesDictionary, TAB_COMMENT_SPLIT, TAB_EQUAL_SPLIT, True, TAB_VALUE_SPLIT)
        continue
      for arch in DataType.ARCH_LIST_FULL + [DataType.TAB_ARCH_NULL]:
        for key in self.KeyList:
          if arch != DataType.TAB_ARCH_NULL:
            target = (key + DataType.TAB_SPLIT + arch).upper()
          else:
            target = key.upper()
          if tab == target:
            if arch != DataType.TAB_ARCH_NULL:
              Command = 'self.ParseDec(sect, tab, self.Contents[arch].' + key + ')'
              eval(Command)
              continue
            else:
              Command = "self.ParseDec(sect, tab, self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ')'
              eval(Command)
              continue
    #EndFor

  def showDec(self):
    print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
    printDict(self.Defines.DefinesDictionary)

    for key in self.KeyList:
      for arch in DataType.ARCH_LIST_FULL:
        Command = "printList(TAB_SECTION_START + '" + \
                  key + DataType.TAB_SPLIT + arch + \
                  "' + TAB_SECTION_END, self.Contents[arch]." + key + ')'
        eval(Command)

if __name__ == '__main__':
  p = Dec()
  directory = 'C:\Documents and Settings\\hchen30\\Desktop\\prototype\\dec'
  fileList = []
  for f in os.listdir(directory):
    if os.path.splitext(os.path.normcase(f))[1] == '.dec':
      fileList.append(os.path.join(directory, os.path.normcase(f)))
      
      
  for f in fileList:
    p.LoadDecFile(f)
    p.showDec()
