#!/usr/bin/env python

#
# Import Modules
#
import os, sys

def TrimPreprocessedFile (source, target, ConvertHex):
  f = open (source,'r')
  lines = f.readlines()
  f.close()
  for index in range (len(lines) - 1, -1, -1):
    if lines[index].strip().find('#line') >= 0:
      index += 1
      break
  else:
    index = 0
  f = open (target,'w')
  for index in range (index, len(lines)):
    if ConvertHex:
      while lines[index].lower().find('0x') >= 0:
        foo=lines[index].lower().find('0x')
        bar = foo + 2
        while lines[index][bar].lower() in '0123456789abcdef':
          bar += 1
        if lines[index][foo+2].lower() in 'abcdef': 
          lines[index] = lines[index][0:foo] + '0' + lines[index][foo+2:bar] + 'h' + lines[index][bar:]
        else:
          lines[index] = lines[index][0:foo] + lines[index][foo+2:bar] + 'h' + lines[index][bar:]
    f.write(lines[index])
  f.close()

if __name__ == '__main__':
  for arg in sys.argv[2:]:
    if sys.argv[1] == '-CONVERT':
      TrimPreprocessedFile(arg, os.path.splitext(arg)[0] + '.iii', True)
    else:
      TrimPreprocessedFile(arg, os.path.splitext(arg)[0] + '.iii', False)
