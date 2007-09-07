## @file
# Convert an XML-based FPD file to a text-based DSC file.
#
# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
import os, re, sys, xml.dom.minidom  #, XmlRoutines, EdkIIWorkspace
from LoadFpd import LoadFpd
from StoreDsc import StoreDsc
from optparse import OptionParser

versionNumber = "1.0"
__version__ = "%prog Version " + versionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."

def myOptionParser():
    """ Argument Parser """
    usage = "%prog [options] input_filename"
    parser = OptionParser(usage=usage,description=__copyright__,version="%prog " + str(versionNumber))
    parser.add_option("-o", "--output", dest="outfile", help="Specific Name of the DSC file to create, otherwise it is the FPD filename with the extension repalced.")
    parser.add_option("-a", "--auto", action="store_true", dest="autowrite", default=False, help="Automatically create output files and write the DSC file")
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive", default=False, help="Set Interactive mode, user must approve each change.")
    parser.add_option("-q", "--quiet", action="store_const", const=0, dest="verbose", help="Do not print any messages, just return either 0 for succes or 1 for failure")
    parser.add_option("-v", "--verbose", action="count", dest="verbose", help="Do not print any messages, just return either 0 for succes or 1 for failure")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Enable printing of debug messages.")
    parser.add_option("-c", "--convert", action="store_true", dest="convert", default=False, help="Convert package: OldMdePkg->MdePkg EdkModulePkg->MdeModulePkg.")
    parser.add_option("-e", "--event", action="store_true", dest="event", default=False, help="Enable handling of Exit Boot Services & Virtual Address Changed Event")
    parser.add_option("-m", "--manual", action="store_true", dest="manual", default=False, help="Generate CommonHeader.txt, user picks up & copy it to a module common header")
    parser.add_option("-w", "--workspace", dest="workspace", default=str(os.environ.get('WORKSPACE')), help="Specify workspace directory.")
    (options, args) = parser.parse_args(sys.argv[1:])

    return options,args

## Entrance method
#
# This method mainly dispatch specific methods per the command line options.
# If no error found, return zero value so the caller of this tool can know
# if it's executed successfully or not.
#
# @retval 0     Tool was successful.
# @retval 1     Tool failed.
#
def Main():
    global options
    global args
    global workspace
    options,args = myOptionParser()
    
    workspace = ""

    if (options.workspace == None):
        print "ERROR: E0000: WORKSPACE not defined.\n  Please set the WORKSPACE environment variable to the location of the EDK II install directory."
        sys.exit(1)
    else:
        workspace = options.workspace
        #print workspace
        if (options.debug):
            print "Using Workspace:", workspace
    try:
        options.verbose +=1
    except:
        options.verbose = 1
        pass

    InputFile = args[0]

    if InputFile != "":
        filename = InputFile
        if ((options.verbose > 1) | (options.autowrite)):
            print "FileName:",InputFile
    else:
        print "ERROR: E0001 - You must specify an input filename"
        sys.exit(1)

    if (options.outfile):
        outputFile = options.outfile
    else:
       outputFile = filename.replace('.fpd', '.dsc')

    if ((options.verbose > 2) or (options.debug)):
        print "Output Filename:", outputFile
        
    try:
        Platform = LoadFpd(filename)
        StoreDsc(options.outfile, Platform)
        return 0
    except Exception, e:
        print e
        return 1

if __name__ == '__main__':
    sys.exit(Main())
    #pass