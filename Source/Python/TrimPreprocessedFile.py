#!/usr/bin/env python

#
# Import Modules
#
import os, sys, re

cTypedefPattern = re.compile("^\s*typedef\s+struct\s+\{", re.MULTILINE)
cPragmaPattern = re.compile("^\s*#pragma\s+pack", re.MULTILINE)

def TrimPreprocessedFile (source, target, Convert, Vfr=False):
    f = open (source,'r')
    lines = f.readlines()
    f.close()

    for index in range (len(lines) - 1, -1, -1):
        if lines[index].strip().find('#line') >= 0:
            endOfCode = index + 1
            break
    else:
        index = 0

    f = open (target,'w')
    if Vfr:
        TrimVfr(lines, 0, endOfCode)
        f.writelines(lines)
    else:
        if Convert:
            ConvertHex(lines, endOfCode, len(lines))
        f.writelines(lines[endOfCode:])
    f.close()

def TrimVfr(lines, start, end):
    foundTypedef = False
    brace = 0
    for index in range (start, end):
        if lines[index].strip().find('#line') == 0:
            continue

        if foundTypedef == False and cTypedefPattern.search(lines[index]) == None:
            if cPragmaPattern.search(lines[index]) == None:
                lines[index] = "\n"
            continue
        elif foundTypedef == False:
            foundTypedef = True

        if lines[index].find("{") >= 0:
            brace += 1
        elif lines[index].find("}") >= 0:
            brace -= 1

        if brace == 0 and lines[index].find(";") >= 0:
##            if lines[index].find("typedef") >= 0:
##                lines[index] = "\n"
            foundTypedef = False

def ConvertHex(lines, start, end):
    for index in range (start, end):
        while lines[index].lower().find('0x') >= 0:
            foo=lines[index].lower().find('0x')
            bar = foo + 2
            while lines[index][bar].lower() in '0123456789abcdef':
                bar += 1
            if lines[index][foo+2].lower() in 'abcdef': 
                lines[index] = lines[index][0:foo] + '0' + lines[index][foo+2:bar] + 'h' + lines[index][bar:]
            else:
                lines[index] = lines[index][0:foo] + lines[index][foo+2:bar] + 'h' + lines[index][bar:]

if __name__ == '__main__':
    if sys.argv[1] == '-CONVERT':
        TrimPreprocessedFile(sys.argv[2], os.path.splitext(sys.argv[2])[0] + '.iii', True)
    elif sys.argv[1] == '-VFR':
        TrimPreprocessedFile(sys.argv[2], os.path.splitext(sys.argv[2])[0] + '.iii', False, True)
    else:
        TrimPreprocessedFile(sys.argv[1], os.path.splitext(sys.argv[1])[0] + '.iii', False)
