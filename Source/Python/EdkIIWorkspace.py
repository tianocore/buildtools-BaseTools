# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This is the base class for applications that operate on an EDK II Workspace 
#

import os, sys, time
from XmlRoutines import *
from DataType import *

class EdkIIWorkspace:
  def __init__(self):
    """Collect WorkspaceDir from the environment, the Verbose command line flag, and detect an icon bitmap file."""

    self.StartTime = time.time()
    self.PrintRunTime   = False
    self.PrintRunStatus = False
    self.RunStatus      = ''
    
    if os.environ.get('WORKSPACE') == None:
      print 'ERROR: WORKSPACE not defined.  Please run EdkSetup from the EDK II install directory.'
      return False

    self.CurrentWorkingDir = os.getcwd()
    
    self.WorkspaceDir = os.path.realpath(os.environ.get('WORKSPACE'))
    (Drive, Path) = os.path.splitdrive(self.WorkspaceDir)
    if Drive == '':
      (Drive, CwdPath) = os.path.splitdrive(self.CurrentWorkingDir)
      if Drive != '':
        self.WorkspaceDir = Drive + Path
    else:
      self.WorkspaceDir = Drive.upper() + Path

    self.WorkspaceRelativeWorkingDir = self.WorkspaceRelativePath (self.CurrentWorkingDir)
      
    try:
      self.Icon = wx.Icon(self.WorkspaceFile('tools/Python/TianoCoreOrgLogo.gif'),wx.BITMAP_TYPE_GIF)
    except:
      self.Icon = None
      
    self.Verbose = False
    for arg in sys.argv:
      if arg.lower() == '-v':
        self.Verbose = True      

    #return True

  def Close(self):
    if self.PrintRunTime:
      Seconds = int(time.time() - self.StartTime)
      if Seconds < 60:
        print 'Run Time: %d seconds' % (Seconds)
      else:
        Minutes = Seconds / 60
        Seconds = Seconds % 60
        if Minutes < 60:
          print 'Run Time: %d minutes %d seconds' % (Minutes, Seconds)
        else:
          Hours = Minutes / 60
          Minutes = Minutes % 60
          print 'Run Time: %d hours %d minutes %d seconds' % (Hours, Minutes, Seconds)
    if self.RunStatus != '':
      print self.RunStatus
    
  def WorkspaceRelativePath(self, FileName):
    """Convert a full path filename to a workspace relative filename."""
    FileName = os.path.realpath(FileName)
    if FileName.find(self.WorkspaceDir) != 0:
      return None
    return FileName.replace (self.WorkspaceDir, '').strip('\\').strip('/')

  def WorkspaceFile(self, FileName):
    """Convert a workspace relative filename to a full path filename."""
    return os.path.realpath(os.path.join(self.WorkspaceDir,FileName))

  def WorkspacePathConvert(self, FileName):
    """Convert ${WORKSPACE} to real path"""
    return os.path.realpath(FileName.replace(TAB_WORKSPACE, self.WorkspaceDir))
    
  def XmlParseFile (self, FileName):
    """Parse an XML file into a DOM and return the DOM."""
    if self.Verbose:
      print FileName
    return XmlParseFile (self.WorkspaceFile(FileName))
    
  def XmlParseFileSection (self, FileName, SectionTag):
    """Parse a section of an XML file into a DOM(Document Object Model) and return the DOM."""
    if self.Verbose:
      print FileName
    return XmlParseFileSection (self.WorkspaceFile(FileName), SectionTag)    

  def XmlSaveFile (self, Dom, FileName):
    """Save a DOM(Document Object Model) into an XML file."""
    if self.Verbose:
      print FileName
    return XmlSaveFile (Dom, self.WorkspaceFile(FileName))

  def ConvertTextFileToDictionary(self, FileName, Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter):
    """Convert a workspace relative text file to a dictionary of (name:value) pairs."""
    if self.Verbose:
      print FileName
    return ConvertTextFileToDictionary(self.WorkspaceFile(FileName), Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter)
  
  def ConvertDictionaryToTextFile(self, FileName, Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter):
    """Convert a dictionary of (name:value) pairs to a workspace relative text file."""
    if self.Verbose:
      print FileName
    return ConvertDictionaryToTextFile(self.WorkspaceFile(FileName), Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter)

#
# Convert a text file to a dictionary
#
def ConvertTextFileToDictionary(FileName, Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter):
  """Convert a text file to a dictionary of (name:value) pairs."""
  try:
    f = open(FileName,'r')
  except:
    return False
  Keys = []
  for Line in f:
    LineList = Line.split(KeySplitCharacter,1)
    if len(LineList) >= 2:
      Key = LineList[0].split()
      if len(Key) == 1 and Key[0][0] != CommentCharacter and Key[0] not in Keys: 
        if ValueSplitFlag:
          Dictionary[Key[0]] = LineList[1].replace('\\','/').split(ValueSplitCharacter)
        else:
          Dictionary[Key[0]] = LineList[1].strip().replace('\\','/')
        Keys += [Key[0]]
  f.close()
  return True

def ConvertDictionaryToTextFile(FileName, Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter):
  """Convert a dictionary of (name:value) pairs to a text file."""
  try:
    f = open(FileName,'r')
    Lines = []
    Lines = f.readlines()
    f.close()
  except:
    Lines = []
  Keys = Dictionary.keys()
  MaxLength = 0
  for Key in Keys:
    if len(Key) > MaxLength:
      MaxLength = len(Key)
  Index = 0
  for Line in Lines:
    LineList = Line.split(KeySplitCharacter,1)
    if len(LineList) >= 2:
      Key = LineList[0].split()
      if len(Key) == 1 and Key[0][0] != CommentCharacter and Key[0] in Dictionary:
        if ValueSplitFlag:
          Line = '%-*s %c %s\n' % (MaxLength, Key[0], KeySplitCharacter, ' '.join(Dictionary[Key[0]]))
        else:
          Line = '%-*s %c %s\n' % (MaxLength, Key[0], KeySplitCharacter, Dictionary[Key[0]])
        Lines.pop(Index)
        if Key[0] in Keys:
          Lines.insert(Index,Line)
          Keys.remove(Key[0])
    Index += 1
  for RemainingKey in Keys:
    if ValueSplitFlag:
      Line = '%-*s %c %s\n' % (MaxLength, RemainingKey, KeySplitCharacter,' '.join(Dictionary[RemainingKey])) 
    else:
      Line = '%-*s %c %s\n' % (MaxLength, RemainingKey, KeySplitCharacter, Dictionary[RemainingKey])
    Lines.append(Line)
  try:
    f = open(FileName,'w')
  except:
    return False
  f.writelines(Lines)
  f.close()
  return True

def CreateDirectory(Directory):
  if not os.access(Directory, os.F_OK):
    os.makedirs (Directory)
  
def CreateFile(Directory, FileName, mode='w'):
  CreateDirectory (Directory)
  return open(os.path.join(Directory, FileName), mode)

# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
  # Nothing to do here. Could do some unit tests
  pass