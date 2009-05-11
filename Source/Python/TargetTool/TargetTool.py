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
import sys
import traceback
from optparse import OptionParser

import Common.EdkLogger as EdkLogger
import Common.BuildToolError as BuildToolError
from Common.DataType import *

# To Do 1.set clean, 2. add item, if the line is disabled.

class TargetTool():
    def __init__(self, opt, args):
        self.WorkSpace = os.getenv('WORKSPACE')
        self.Opt       = opt
        self.Arg       = args[0]
        self.FileName  = os.path.normpath(os.path.join(self.WorkSpace, 'Conf\\target.txt'))
        if os.path.isfile(self.FileName) == False:
            print "%s does not exist." % self.FileName
            sys.exit(1)
        self.TargetTxtDictionary = {
            TAB_TAT_DEFINES_ACTIVE_PLATFORM                            : '',
            TAB_TAT_DEFINES_TOOL_CHAIN_CONF                            : '',
            TAB_TAT_DEFINES_MULTIPLE_THREAD                            : '',
            TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER               : '',
            TAB_TAT_DEFINES_TARGET                                     : [''],
            TAB_TAT_DEFINES_TOOL_CHAIN_TAG                             : [''],
            TAB_TAT_DEFINES_TARGET_ARCH                                : [''],
            TAB_TAT_DEFINES_BUILD_RULE_CONF                            : [''],
        }
        self.LoadTargetTxtFile(self.FileName)

    def LoadTargetTxtFile(self, filename):
        if os.path.exists(filename) and os.path.isfile(filename):
             return self.ConvertTextFileToDict(filename, '#', '=')
        else:
            raise ParseError('LoadTargetTxtFile() : No Target.txt file exists.')
            return 1

#
# Convert a text file to a dictionary
#
    def ConvertTextFileToDict(self, FileName, CommentCharacter, KeySplitCharacter):
        """Convert a text file to a dictionary of (name:value) pairs."""
        try:
            f = open(FileName,'r')
            for Line in f:
                if Line.startswith(CommentCharacter) or Line.strip() == '':
                    continue
                LineList = Line.split(KeySplitCharacter,1)
                if len(LineList) >= 2:
                    Key = LineList[0].strip()
                    if Key.startswith(CommentCharacter) == False and Key in self.TargetTxtDictionary.keys():
                        if Key == TAB_TAT_DEFINES_ACTIVE_PLATFORM or Key == TAB_TAT_DEFINES_TOOL_CHAIN_CONF \
                          or Key == TAB_TAT_DEFINES_MULTIPLE_THREAD or Key == TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER \
                          or Key == TAB_TAT_DEFINES_ACTIVE_MODULE:
                            self.TargetTxtDictionary[Key] = LineList[1].replace('\\', '/').strip()
                        elif Key == TAB_TAT_DEFINES_TARGET or Key == TAB_TAT_DEFINES_TARGET_ARCH \
                          or Key == TAB_TAT_DEFINES_TOOL_CHAIN_TAG or Key == TAB_TAT_DEFINES_BUILD_RULE_CONF:
                            self.TargetTxtDictionary[Key] = LineList[1].split()
            f.close()
            return 0
        except:
            last_type, last_value, last_tb = sys.exc_info()
            traceback.print_exception(last_type, last_value, last_tb)

    def Print(self):
        KeyList = self.TargetTxtDictionary.keys()
        for Key in KeyList:
            if type(self.TargetTxtDictionary[Key]) == type([]):
                print "%-30s = %s" % (Key, ''.join(elem + ' ' for elem in self.TargetTxtDictionary[Key]))
            else:
                print "%-30s = %s" % (Key, self.TargetTxtDictionary[Key])

    def RWFile(self, CommentCharacter, KeySplitCharacter, Num):
        try:
            fr = open(self.FileName, 'r')
            fw = open(os.path.normpath(os.path.join(self.WorkSpace, 'Conf\\targetnew.txt')), 'w')

            for Line in fr:
                if Line.startswith(CommentCharacter) or Line.strip() == '':
                    fw.write(Line)
                else:
                    LineList = Line.split(KeySplitCharacter,1)
                    if len(LineList) >= 2:
                        Key = LineList[0].strip()
                        if Key.startswith(CommentCharacter) == False and Key in self.TargetTxtDictionary.keys():
                            if Num == 0:
                                Line = "%-30s = \n" % Key
                            else:
                                if Key == TAB_TAT_DEFINES_ACTIVE_PLATFORM:
                                    if self.Opt.DSCFILE == '0':
                                        Line = "%-30s = \n" % Key
                                    elif self.Opt.DSCFILE != None:
                                        dscFullPath = os.path.join(self.WorkSpace, self.Opt.DSCFILE)
                                        if os.path.exists(dscFullPath):
                                            Line = "%-30s = %s\n" % (Key, self.Opt.DSCFILE)
                                        else:
                                            EdkLogger.error("TagetTool", BuildToolError.FILE_NOT_FOUND, 
                                                                   "DSC file %s does not exist!" % self.Opt.DSCFILE, RaiseError=False)
                                    else:
                                        pass
                                elif Key == TAB_TAT_DEFINES_TOOL_CHAIN_CONF:
                                    if self.Opt.TOOL_DEFINITION_FILE == '0':
                                        Line = "%-30s = \n" % Key
                                    elif self.Opt.TOOL_DEFINITION_FILE != None:
                                        tooldefFullPath = os.path.join(self.WorkSpace, self.Opt.TOOL_DEFINITION_FILE)
                                        if os.path.exists(tooldefFullPath):
                                            Line = "%-30s = %s\n" % (Key, self.Opt.TOOL_DEFINITION_FILE)
                                        else:
                                            EdkLogger.error("TagetTool", BuildToolError.FILE_NOT_FOUND, 
                                                                   "Tooldef file %s does not exist!" % self.Opt.TOOL_DEFINITION_FILE, RaiseError=False)
                                    else:
                                        pass
                                elif Key == TAB_TAT_DEFINES_MULTIPLE_THREAD and self.Opt.NUM != None:
                                    if self.Opt.NUM >= 2:
                                        Line = "%-30s = %s\n" % (Key, 'Enable')
                                    else:
                                        Line = "%-30s = %s\n" % (Key, 'Disable')
                                elif Key == TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER:
                                    if self.Opt.NUM != None:
                                        Line = "%-30s = %s\n" % (Key, str(self.Opt.NUM))

                                elif Key == TAB_TAT_DEFINES_TARGET:
                                    if self.Opt.TARGET == ['0']:
                                        Line = "%-30s = \n" % Key
                                    elif self.Opt.TARGET != None:
                                        Line = "%-30s = %s\n" % (Key, ''.join(elem + ' ' for elem in self.Opt.TARGET))
                                    else:
                                        pass
                                elif Key == TAB_TAT_DEFINES_TARGET_ARCH:
                                    if self.Opt.TARGET_ARCH == ['0']:
                                        Line = "%-30s = \n" % Key
                                    elif self.Opt.TARGET_ARCH != None:
                                        Line = "%-30s = %s\n" % (Key, ''.join(elem + ' ' for elem in self.Opt.TARGET_ARCH))
                                    else:
                                        pass
                                elif Key == TAB_TAT_DEFINES_TOOL_CHAIN_TAG:
                                    if self.Opt.TOOL_CHAIN_TAG == '0':
                                        Line = "%-30s = \n" % Key
                                    elif self.Opt.TOOL_CHAIN_TAG != None:
                                        Line = "%-30s = %s\n" % (Key, self.Opt.TOOL_CHAIN_TAG)
                                    else:
                                        pass
                                elif Key == TAB_TAT_DEFINES_BUILD_RULE_CONF:
                                    if self.Opt.BUILD_RULE_FILE == '0':
                                        Line = "%-30s = \n" % Key
                                    elif self.Opt.BUILD_RULE_FILE != None:
                                        buildruleFullPath = os.path.join(self.WorkSpace, self.Opt.BUILD_RULE_FILE)
                                        if os.path.exists(buildruleFullPath):
                                            Line = "%-30s = %s\n" % (Key, self.Opt.BUILD_RULE_FILE)
                                        else:
                                            EdkLogger.error("TagetTool", BuildToolError.FILE_NOT_FOUND, 
                                                            "Build rule file %s does not exist!" % self.Opt.BUILD_RULE_FILE, RaiseError=False)
                                            
                                    else:
                                        pass                                    
                                else:
                                    pass
                            fw.write(Line)
            fr.close()
            fw.close()
            os.remove(self.FileName)
            os.rename(os.path.normpath(os.path.join(self.WorkSpace, 'Conf\\targetnew.txt')), self.FileName)
            
        except:
            last_type, last_value, last_tb = sys.exc_info()
            traceback.print_exception(last_type, last_value, last_tb)


VersionNumber = "0.01"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."
__usage__ = "%prog [options] {args} \
\nArgs:                                                  \
\n Clean  clean the all default configuration of target.txt. \
\n Print  print the all default configuration of target.txt. \
\n Set    replace the default configuration with expected value specified by option."

def MyOptionParser():
    parser = OptionParser(version=__version__,prog="TargetTool.exe",usage=__usage__,description=__copyright__)
    parser.add_option("-a", "--arch", action="append", type="choice", choices=['IA32','X64','IPF','EBC','0'], dest="TARGET_ARCH",
        help="ARCHS is one of list: IA32, X64, IPF or EBC, which replaces target.txt's TARGET_ARCH definition. To specify more archs, please repeat this option. 0 will clear this setting in target.txt and can't combine with other value.")
    parser.add_option("-p", "--platform", action="store", type="string", dest="DSCFILE",
        help="Specify a DSC file, which replace target.txt's ACTIVE_PLATFORM definition. 0 will clear this setting in target.txt and can't combine with other value.")
    parser.add_option("-c", "--tooldef", action="store", type="string", dest="TOOL_DEFINITION_FILE",
        help="Specify the WORKSPACE relative path of tool_def.txt file, which replace target.txt's TOOL_CHAIN_CONF definition. 0 will clear this setting in target.txt and can't combine with other value.")
    parser.add_option("-t", "--target", action="append", type="choice", choices=['DEBUG','RELEASE','0'], dest="TARGET",
        help="TARGET is one of list: DEBUG, RELEASE, which replaces target.txt's TARGET definition. To specify more TARGET, please repeat this option. 0 will clear this setting in target.txt and can't combine with other value.")
    parser.add_option("-n", "--tagname", action="store", type="string", dest="TOOL_CHAIN_TAG",
        help="Specify the Tool Chain Tagname, which replaces target.txt's TOOL_CHAIN_TAG definition. 0 will clear this setting in target.txt and can't combine with other value.")
    parser.add_option("-r", "--buildrule", action="store", type="string", dest="BUILD_RULE_FILE",
        help="Specify the build rule configure file, which replaces target.txt's BUILD_RULE_CONF definition. If not specified, the default value Conf/build_rule.txt will be set.")
    parser.add_option("-m", "--mutlithread", action="store", type="int", dest="NUM",
        help="Specify the multi-threaded number which replace target.txt's MAX_CONCURRENT_THREAD_NUMBER. If the value is less than 2, MULTIPLE_THREAD will be disabled. If the value is larger than 1, MULTIPLE_THREAD will be enabled.")

    (opt, args)=parser.parse_args()
    return (opt, args)

if __name__ == '__main__':
    EdkLogger.Initialize()
    EdkLogger.SetLevel(EdkLogger.QUIET)
    (opt, args) = MyOptionParser()
    if len(args) != 1 or (args[0].lower() != 'print' and args[0].lower() != 'clean' and args[0].lower() != 'set'):
        print "The number of args isn't 1 or the value of args is invalid."
        sys.exit(1)
    if opt.NUM != None and opt.NUM < 1:
        print "The MAX_CONCURRENT_THREAD_NUMBER must be larger than 0."
        sys.exit(1)
    if opt.TARGET != None and len(opt.TARGET) > 1:
        for elem in opt.TARGET:
            if elem == '0':
                print "0 will clear the TARGET setting in target.txt and can't combine with other value."
                sys.exit(1)
    if opt.TARGET_ARCH != None and len(opt.TARGET_ARCH) > 1:
        for elem in opt.TARGET_ARCH:
            if elem == '0':
                print "0 will clear the TARGET_ARCH setting in target.txt and can't combine with other value."
                sys.exit(1)

    try:
        FileHandle = TargetTool(opt, args)
        if FileHandle.Arg.lower() == 'print':
            FileHandle.Print()
            sys.exit(0)
        elif FileHandle.Arg.lower() == 'clean':
            FileHandle.RWFile('#', '=', 0)
        else:
            FileHandle.RWFile('#', '=', 1)
    except Exception, e:
        last_type, last_value, last_tb = sys.exc_info()
        traceback.print_exception(last_type, last_value, last_tb)

