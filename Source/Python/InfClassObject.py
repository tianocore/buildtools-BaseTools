# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define each component of INF file
#

import os
import EdkLogger
from String import *
from DataType import *
from Identification import *
from Dictionary import *

class InfObject(object):
  def __init__(self):
    object.__init__()

class InfDefines(InfObject):
  def __init__(self):
    self.DefinesDictionary = {
      #Required
      TAB_INF_DEFINES_BASE_NAME                    : '',
      TAB_INF_DEFINES_EDK_RELEASE_VERSION          : '',
      TAB_INF_DEFINES_EFI_SPECIFICATION_VERSION    : '',
      #Optional
      TAB_INF_DEFINES_FILE_GUID                    : '',
      TAB_INF_DEFINES_MODULE_TYPE                  : '',
      TAB_INF_DEFINES_BINARY_MODULE                : '',
      TAB_INF_DEFINES_MAKEFILE_NAME                : '',
      TAB_INF_DEFINES_VERSION_STRING               : '',
      TAB_INF_DEFINES_VERSION                      : '',
      TAB_INF_DEFINES_LIBRARY_CLASS                : '',
      TAB_INF_DEFINES_PCD_DRIVER                   : '',
      TAB_INF_DEFINES_ENTRY_POINT                  : [],
      TAB_INF_DEFINES_UNLOAD_IMAGE                 : [],
      TAB_INF_DEFINES_CONSTRUCTOR                  : [],
      TAB_INF_DEFINES_DESTRUCTOR                   : [],
      TAB_INF_DEFINES_DEFINE                       : '',
      TAB_INF_DEFINES_CUSTOM_MAKEFILE              : '',
      TAB_INF_DEFINES_INF_VERSION                  : ''
    }
    self.ToolFlags = []   #'${FAMILY}:${TARGET}_${TAGNAME}_${ARCH}_${TOOLCODE}_FLAGS'
    self.MacroName = '$(MACRO_NAME)'

class InfContents(InfObject):
  def __init__(self):
    self.Sources = []
    self.BuildOptions = []
    self.Binaries = []
    self.Includes = []
    self.Guids = []
    self.Protocols = []
    self.Ppis = []
    self.LibraryClasses = []
    self.Packages = []
    self.PcdsFixedAtBuild = []
    self.PcdsPatchableInModule = []
    self.PcdsFeatureFlag = []
    self.PcdsDynamic = []
    self.PcdsDynamicEx = []
    self.Depex = []
    
class Inf(InfObject):
  def __init__(self, filename = None, isMergeAllArches = False):
    self.identification = Identification()
    self.Defines = InfDefines()
    self.Contents = {}
    
    for key in DataType.ARCH_LIST_FULL:
      self.Contents[key] = InfContents()

    self.KeyList = [
      TAB_BINARIES, TAB_SOURCES, TAB_INCLUDES, TAB_GUIDS, TAB_PROTOCOLS, TAB_PPIS, TAB_LIBRARY_CLASSES, TAB_PACKAGES, TAB_BUILD_OPTIONS, \
      TAB_PCDS_FIXED_AT_BUILD_NULL, TAB_PCDS_PATCHABLE_IN_MODULE_NULL, TAB_PCDS_FEATURE_FLAG_NULL, \
      TAB_PCDS_DYNAMIC_NULL, TAB_PCDS_DYNAMIC_EX_NULL
    ]
        
    if filename != None:
      self.LoadInfFile(filename)
    
    if isMergeAllArches:
      self.MergeAllArches()
  
  def MergeAllArches(self):
    for key in self.KeyList:
      for arch in DataType.ARCH_LIST:
        Command = "self.Contents[arch]." + key + ".extend(" + "self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ")"
        eval(Command)   
      
  def ParseInf(self, Lines, Key, KeyField):
      GetMultipleValuesOfKeyFromLines(Lines, Key, KeyField, TAB_COMMENT_SPLIT)

  def LoadInfFile(self, filename):   
    (filepath, name) = os.path.split(filename)
    self.identification.FileName = name
    self.identification.FileFullPath = filename
    self.identification.FileRelativePath = filepath
    
    f = open(filename, 'r').read()
    sects = f.split('[')
    for sect in sects:
      tab = (sect.split(TAB_SECTION_END, 1)[0]).upper()
      if tab == TAB_INF_DEFINES.upper():
        GetSingleValueOfKeyFromLines(sect, self.Defines.DefinesDictionary, TAB_COMMENT_SPLIT, TAB_EQUAL_SPLIT, False, None)
        continue
      for arch in DataType.ARCH_LIST_FULL + [DataType.TAB_ARCH_NULL]:
        for key in self.KeyList:
          if arch != DataType.TAB_ARCH_NULL:
            target = (key + DataType.TAB_SPLIT + arch).upper()
          else:
            target = key.upper()
          if tab == target:
            if arch != DataType.TAB_ARCH_NULL:
              Command = 'self.ParseInf(sect, tab, self.Contents[arch].' + key + ')'
              eval(Command)
              continue
            else:
              Command = "self.ParseInf(sect, tab, self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ')'
              eval(Command)
              continue
    #EndFor

  def showInf(self):
    print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
    printDict(self.Defines.DefinesDictionary)

    for key in self.KeyList:
      for arch in DataType.ARCH_LIST_FULL:
        Command = "printList(TAB_SECTION_START + '" + \
                  key + DataType.TAB_SPLIT + arch + \
                  "' + TAB_SECTION_END, self.Contents[arch]." + key + ')'
        eval(Command)
    print ""
    
if __name__ == '__main__':
  m = Inf()
  directory = 'C:\Documents and Settings\\hchen30\\Desktop\\prototype\\inf'
  fileList = []
  
  for f in os.listdir(directory):
    if os.path.splitext(os.path.normcase(f))[1] == '.inf':
      fileList.append(os.path.join(directory, os.path.normcase(f)))
      
  for f in fileList:
    m = Inf(f)
    m.showInf()
