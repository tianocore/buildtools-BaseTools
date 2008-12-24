## @file
# This file is used to define a class object to describe a distribution package
#
# Copyright (c) 2008, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

##
# Import Modules
#
import os.path
from CommonClass import *
from CommonDataClass.CommonClass import FileClass
from Common.Misc import sdict
from Common.Misc import GetFiles
from Common.DecClassObjectLight import Dec
from Common.InfClassObjectLight import Inf
from Common.XmlParser import *

## DistributionPackageHeaderClass
#
class DistributionPackageHeaderClass(IdentificationClass, CommonHeaderClass):
    def __init__(self):
        IdentificationClass.__init__(self)
        CommonHeaderClass.__init__(self)
        self.ReadOnly = 'False'
        self.RePackage = 'True'
        self.Vendor = ''
        self.Date = ''
        self.Signature = 'Md5Sum'
        self.XmlSpecification = ''

## DistributionPackageClass
#
#
class DistributionPackageClass(object):
    def __init__(self):
        self.Header = DistributionPackageHeaderClass()
        self.PackageSurfaceArea = sdict() # {(Guid, Version, Path) : PackageObj}
        self.ModuleSurfaceArea = sdict()  # {(Guid, Version, Path) : ModuleObj}
        self.Tools = MiscFileClass()
        self.MiscellaneousFiles = MiscFileClass()
        self.UserExtensions = []
    
    ## Get all included packages and modules for a distribution package
    # 
    # @param WorkspaceDir:  WorkspaceDir
    # @param PackageList:   A list of all packages
    # @param ModuleList:    A list of all modules
    #
    def GetDistributionPackage(self, WorkspaceDir, PackageList, ModuleList):
        # Get Packages
        if PackageList:
            for PackageFile in PackageList:
                PackageFileFullPath = os.path.normpath(os.path.join(WorkspaceDir, PackageFile))
                DecObj = Dec(PackageFileFullPath, True, WorkspaceDir)
                PackageObj = DecObj.Package
                # Get all files under the package
                PackageFileList = GetFiles(DecObj.Identification.FileRelativePath, ['CVS', '.svn'])
                # Remove dec file itself
                PackageFileList.remove(PackageFileFullPath)
                # Remove files found in dec parser
                for File in PackageObj.FileList:
                    if File in PackageFileList:
                        PackageFileList.remove(File)
                # Parser inf file one bye one
                for File in PackageFileList:
                    (Name, ExtName) = os.path.splitext(File)
                    if ExtName.upper() == '.INF':
                        InfObj = Inf(File, True, WorkspaceDir, DecObj.Identification.PackagePath)
                        ModuleObj = InfObj.Module
                        PackageObj.Modules[(ModuleObj.ModuleHeader.Guid, ModuleObj.ModuleHeader.Version, ModuleObj.ModuleHeader.RelaPath)] = ModuleObj
                        PackageFileList.remove(File)
                        for ModuleFile in ModuleObj.FileList:
                            if ModuleFile in PackageFileList:
                                PackageFileList.remove(ModuleFile)
                for File in PackageFileList:
                    FileObj = FileClass()
                    FileObj.Filename = File[len(DecObj.Identification.FileRelativePath) + 1:]
                    PackageObj.MiscFiles.Files.append(FileObj)
                self.PackageSurfaceArea[(PackageObj.PackageHeader.Guid, PackageObj.PackageHeader.Version, PackageObj.PackageHeader.FullPath)] = PackageObj

        # Get Modules
        if ModuleList:
            for ModuleFile in ModuleList:
                ModuleFileFullPath = os.path.normpath(os.path.join(WorkspaceDir, ModuleFile))
                InfObj = Inf(ModuleFileFullPath, True, WorkspaceDir)
                ModuleObj = InfObj.Module
                # Get all files under the module
                ModuleFileList = GetFiles(InfObj.Identification.FileRelativePath, ['CVS', '.svn'])
                # Remove dec file itself
                ModuleFileList.remove(ModuleFileFullPath)
                # Remove files found in dec parser
                for File in ModuleObj.FileList:
                    if File in ModuleFileList:
                        ModuleFileList.remove(File)
                for File in ModuleFileList:
                    FileObj = FileClass()
                    FileObj.Filename = File[len(InfObj.Identification.FileRelativePath) + 1:]
                    ModuleObj.MiscFiles.Files.append(FileObj)
                self.ModuleSurfaceArea[(ModuleObj.ModuleHeader.Guid, ModuleObj.ModuleHeader.Version, ModuleObj.ModuleHeader.FullPath)] = ModuleObj

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    pass
    #D = DistributionPackage()
    #D.GetDistributionPackage(os.getenv('WORKSPACE'), ['MdePkg/MdePkg.dec', 'TianoModulePkg/TianoModulePkg.dec'], ['MdeModulePkg/Application/HelloWorld/HelloWorld.inf'], 'C:\\MyWork\\DpHeaderTemplate.xml')
    #D.GetDistributionPackage(os.getenv('WORKSPACE'), ['MdePkg/MdePkg.dec'], ['MdeModulePkg/Application/HelloWorld/HelloWorld.inf'], None)
    #Xml = DistributionPackageXml()
    #print Xml.ToXml(D)
    #print 'END 1'
    #E = Xml.FromXml('C:\\2.xml')
    #print Xml.ToXml(E)
    #print 'END 2'
