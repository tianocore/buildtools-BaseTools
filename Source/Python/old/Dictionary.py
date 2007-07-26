import EdkLogger
from DataType import *

#
# Convert a text file to a dictionary
#
def ConvertTextFileToDictionary(FileName, Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter):
  """Convert a text file to a dictionary of (name:value) pairs."""
  try:
    f = open(FileName,'r')
  except:
    EdkLogger.info('Open file failed')
    return False
  Keys = []
  for Line in f:
    if Line.startswith(CommentCharacter):
      continue
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

def printDict(dict):
  if dict != None:
    KeyList = dict.keys()
    for Key in KeyList:
      if dict[Key] != '':
        print Key + ' = ' + str(dict[Key])

def printList(key, list):
  if type(list) == type([]):
      if len(list) > 0:
        if key.find(TAB_SPLIT) != -1:
          print "\n" + key
          for i in list:
            print i
    
      
