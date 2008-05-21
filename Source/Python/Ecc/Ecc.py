## @file
# This file is used to be the main entrance of ECC tool
#
# Copyright (c) 2008, Intel Corporation
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
import os, time, glob
import Common.EdkLogger as EdkLogger
import Database
import EccGlobalData
from MetaDataParser import *
from optparse import OptionParser
from Configuration import Configuration
from Check import Check
from Common.InfClassObject import Inf
from Common.DecClassObject import Dec
from Common.DscClassObject import Dsc
from Common.FdfClassObject import Fdf
from Common.String import NormPath
from Common import BuildToolError
import c

## Ecc
#
# This class is used to define Ecc main entrance
#
# @param object:          Inherited from object class
#
class Ecc(object):
    def __init__(self):
        # Version and Copyright
        self.VersionNumber = "0.01"
        self.Version = "%prog Version " + self.VersionNumber
        self.Copyright = "Copyright (c) 2008, Intel Corporation  All rights reserved."
        
        self.ConfigFile = 'config.ini'
        self.OutputFile = 'output.txt'
        self.IsInit = True
        
        #
        # Parse the options and args
        #
        self.ParseOption()

        #
        # Generate checkpoints list
        #
        EccGlobalData.gConfig = Configuration(self.ConfigFile)
        
        #
        # Init Ecc database
        #
        EccGlobalData.gDb = Database.Database(Database.DATABASE_PATH)
        EccGlobalData.gDb.InitDatabase(self.IsInit)
        
        #
        # Build ECC database
        #
        self.BuildDatabase()
        
        #
        # Start to check
        #
        self.Check()
        
        #
        # Show report
        #
        self.GenReport()
        
        #
        # Close Database
        #
        EccGlobalData.gDb.Close()



    ## BuildDatabase
    #
    # Build the database for target
    #
    def BuildDatabase(self):
        #
        # Clean report table
        #
        EccGlobalData.gDb.TblReport.Drop()
        EccGlobalData.gDb.TblReport.Create()
        
        #
        # Build database
        #
        if self.IsInit:
            EdkLogger.quiet("Building database for source code ...")
            c.CollectSourceCodeDataIntoDB(EccGlobalData.gTarget)
            EdkLogger.quiet("Building database for source code done!")
            self.BuildMetaDataFileDatabase()
        
        EccGlobalData.gIdentifierTableList = GetTableList((MODEL_FILE_C, MODEL_FILE_H), 'Identifier', EccGlobalData.gDb)
    
    ## BuildMetaDataFileDatabase
    #
    # Build the database for meta data files
    #
    def BuildMetaDataFileDatabase(self):
        EdkLogger.quiet("Building database for meta data files ...")
        Op = open(EccGlobalData.gConfig.MetaDataFileCheckPathOfGenerateFileList, 'w+')
        for Root, Dirs, Files in os.walk(EccGlobalData.gTarget):
            if "CVS" in Dirs:
                Dirs.remove('CVS')
            if ".svn" in Dirs:
                Dirs.remove('.svn')
            if "Build" in Dirs:
                Dirs.remove('Build')
            if "EdkCompatibilityPkg" in Dirs:
                Dirs.remove('EdkCompatibilityPkg')
            
            for File in Files:
                if len(File) > 4 and File[-4:].upper() == ".DEC":
                    Filename = os.path.normpath(os.path.join(Root, File))
                    EdkLogger.quiet("Parsing %s" % Filename)
                    Op.write("%s\r" % Filename)
                    Dec(Filename, True, True, EccGlobalData.gWorkspace, EccGlobalData.gDb)
                    continue
                if len(File) > 4 and File[-4:].upper() == ".DSC":
                    Filename = os.path.normpath(os.path.join(Root, File))
                    EdkLogger.quiet("Parsing %s" % Filename)
                    Op.write("%s\r" % Filename)
                    Dsc(Filename, True, True, EccGlobalData.gWorkspace, EccGlobalData.gDb)
                    continue
                if len(File) > 4 and File[-4:].upper() == ".INF":
                    Filename = os.path.normpath(os.path.join(Root, File))
                    EdkLogger.quiet("Parsing %s" % Filename)
                    Op.write("%s\r" % Filename)
                    Inf(Filename, True, True, EccGlobalData.gWorkspace, EccGlobalData.gDb)
                    continue
                if len(File) > 4 and File[-4:].upper() == ".FDF":
                    Filename = os.path.normpath(os.path.join(Root, File))
                    EdkLogger.quiet("Parsing %s" % Filename)
                    Op.write("%s\r" % Filename)
                    Fdf(Filename, True, EccGlobalData.gWorkspace, EccGlobalData.gDb)                    
                    continue
        Op.close()
        
        #
        # Commit to database
        #
        EccGlobalData.gDb.Conn.commit()
        
        EdkLogger.quiet("Building database for meta data files done!")
    
    ##
    #
    # Check each checkpoint
    #
    def Check(self):
        EdkLogger.quiet("Checking ...")
        EccCheck = Check()
        EccCheck.Check()
        EdkLogger.quiet("Checking  done!")
    
    ##
    #
    # Generate the scan report
    #
    def GenReport(self):
        EdkLogger.quiet("Generating report ...")
        EccGlobalData.gDb.TblReport.ToCSV()
        EdkLogger.quiet("Generating report done!")
    
    ## ParseOption
    #
    # Parse options
    #
    def ParseOption(self):
        EdkLogger.quiet("Loading ECC configuration ... done")
        (Options, Target) = self.EccOptionParser()
        
        #
        # Check workspace envirnoment
        #
        if "WORKSPACE" not in os.environ:
            EdkLogger.error("ECC", BuildToolError.ATTRIBUTE_NOT_AVAILABLE, "Environment variable not found", 
                            ExtraData="WORKSPACE")
        else:
            EccGlobalData.gWorkspace = os.path.normpath(os.getenv("WORKSPACE"))
            if not os.path.exists(EccGlobalData.gWorkspace):
                EdkLogger.error("ECC", BuildToolError.FILE_NOT_FOUND, ExtraData="WORKSPACE = %s" % EccGlobalData.gWorkspace)
            os.environ["WORKSPACE"] = EccGlobalData.gWorkspace
        #
        # Set log level
        #
        self.SetLogLevel(Options)
        
        #
        # Set other options
        #
        if Options.ConfigFile != None:
            self.ConfigFile = Options.ConfigFile
        if Options.OutputFile != None:
            self.OutputFile = Options.OutputFile
        if Options.Target != None:
            EccGlobalData.gTarget = os.path.normpath(Options.Target)
        else:
            EdkLogger.warn("Ecc", EdkLogger.ECC_ERROR, "The target source tree was not specified, using current WORKSPACE instead!")
            EccGlobalData.gTarget = os.path.normpath(os.getenv("WORKSPACE"))
        if Options.keepdatabase != None:
            self.IsInit = False
           
    ## SetLogLevel
    #
    # Set current log level of the tool based on args
    #
    # @param Option:  The option list including log level setting 
    #
    def SetLogLevel(self, Option):
        if Option.verbose != None:
            EdkLogger.SetLevel(EdkLogger.VERBOSE)
        elif Option.quiet != None:
            EdkLogger.SetLevel(EdkLogger.QUIET)
        elif Option.debug != None:
            EdkLogger.SetLevel(Option.debug + 1)
        else:
            EdkLogger.SetLevel(EdkLogger.INFO)

    ## Parse command line options
    #
    # Using standard Python module optparse to parse command line option of this tool.
    #
    # @retval Opt   A optparse.Values object containing the parsed options
    # @retval Args  Target of build command
    #
    def EccOptionParser(self):
        Parser = OptionParser(description = self.Copyright, version = self.Version, prog = "Ecc.exe", usage = "%prog [options]")
        Parser.add_option("-t", "--target sourcepath", action="store", type="string", dest='Target',
            help="Check all files under the target workspace.")
        Parser.add_option("-c", "--config filename", action="store", type="string", dest="ConfigFile",
            help="Specify a configuration file. Defaultly use config.ini under ECC tool directory.")
        Parser.add_option("-o", "--outfile filename", action="store", type="string", dest="OutputFile",
            help="Specify the name of an output file, if and only if one filename was specified.")
    
        Parser.add_option("-k", "--keepdatabase", action="store_true", type=None, help="The existing Ecc database will not be cleaned except report information if this option is specified.")
        Parser.add_option("-l", "--log filename", action="store", dest="LogFile", help="""If specified, the tool should emit the changes that 
                                                                                          were made by the tool after printing the result message. 
                                                                                          If filename, the emit to the file, otherwise emit to 
                                                                                          standard output. If no modifications were made, then do not 
                                                                                          create a log file, or output a log message.""")
        Parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
        Parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed, "\
                                                                                   "including library instances selected, final dependency expression, "\
                                                                                   "and warning messages, etc.")
        Parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")
    
        (Opt, Args)=Parser.parse_args()
        
        return (Opt, Args)

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    #
    # Initialize log system
    #
    EdkLogger.Initialize()
    EdkLogger.IsRaiseError = False
    EdkLogger.quiet(time.strftime("%H:%M:%S, %b.%d %Y ", time.localtime()) + "[00:00]" + "\n")

    StartTime = time.clock()
    Ecc = Ecc()
    FinishTime = time.clock()

    BuildDuration = time.strftime("%M:%S", time.gmtime(int(round(FinishTime - StartTime))))
    EdkLogger.quiet("\n%s [%s]" % (time.strftime("%H:%M:%S, %b.%d %Y", time.localtime()), BuildDuration))

