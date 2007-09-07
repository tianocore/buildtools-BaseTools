## @file
# Open an FPD file and load all its contents to a PlatformClass object.
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
import os
from CommonDataClass.PlatformClass import *
from CommonDataClass.FdfClassObject import *
from Common.XmlRoutines import *
from Common.MigrationUtilities import *
from EdkIIWorkspaceGuidsInfo import gEdkIIWorkspaceGuidsInfo

## Load Platform Header.
#
# Read an input Platform XML DOM object and return Platform Header class object
# contained in the DOM object.
#
# @param  XmlFpd                     An XML DOM object read from FPD file.
# @param  FpdFileName           The file path of FPD File.
#
# @retvel  PlatformHeader         A new Platform Header object loaded from XmlFpd.
#
def LoadPlatformHeader(XmlFpd, FpdFileName):
    PlatformHeader = PlatformHeaderClass()
    
    XmlTag = "PlatformSurfaceArea/PlatformHeader"
    FpdHeader = XmlNode(XmlFpd, XmlTag)
    
    SetIdentification(PlatformHeader, FpdHeader, "PlatformName", FpdFileName)
    SetCommonHeader(PlatformHeader, FpdHeader)

    XmlTag = "PlatformSurfaceArea/PlatformDefinitions/SupportedArchitectures"
    PlatformHeader.SupArchList = XmlElement(XmlFpd, XmlTag).split()

    XmlTag = "PlatformSurfaceArea/PlatformDefinitions/BuildTargets"
    PlatformHeader.BuildTargets = XmlElement(XmlFpd, XmlTag).split()

    XmlTag = "PlatformSurfaceArea/PlatformDefinitions/IntermediateDirectories"
    PlatformHeader.IntermediateDirectories = XmlElement(XmlFpd, XmlTag)
    
    XmlTag = "PlatformSurfaceArea/PlatformDefinitions/OutputDirectory"
    PlatformHeader.OutputDirectory = XmlElement(XmlFpd, XmlTag)

    XmlTag = "PlatformSurfaceArea/PlatformDefinitions/SkuInfo"
    List = map(LoadSkuId, XmlList(XmlFpd, XmlTag))
    PlatformHeader.SkuIdName = List[0]

    return PlatformHeader

## Load a Platform SkuId.
#
# Read an input Platform XML DOM object and return a list of Platform SkuId
# contained in the DOM object.
#
# @param    XmlPlatformSkuInfo     An XML DOM object read from FPD file.
#
# @retvel   PlatformSkuInfo        A SkuInfo loaded from XmlFpd.
#
def LoadPlatformSkuInfo(XmlPlatformSkuInfo):
    XmlTag = "SkuInfo/SkuId"
    SkuInfo = []
    SkuId = XmlElement(XmlPlatformSkuInfo, XmlTag)
    SkuInfo.append(SkuId)
    
    XmlTag = "SkuInfo/Value"
    Value = XmlElement(XmlPlatformSkuInfo, XmlTag)
    SkuInfo.append(Value)
    return SkuInfo

def LoadSkuId(XmlSkuInfo):
    XmlTag = "SkuInfo/UiSkuName"
    SkuValue = XmlElement(XmlSkuInfo, XmlTag)
    
    XmlTag = "SkuInfo/UiSkuName/SkuID"
    SkuId = XmlAttribute(XmlSkuInfo, XmlTag)
    List = []
    List.append(SkuId)
    List.append(SkuValue)
    return List

## Load a list of Platform SkuIds.
#
# Read an input Platform XML DOM object and return a list of Platform SkuId
# contained in the DOM object.
#
# @param    XmlFpd                 An XML DOM object read from FPD file.
#
# @retvel   PlatformSkuIds                A list of SkuIds loaded from XmlFpd.
#
def LoadPlatformSkuInfos(XmlFpd):
    PlatformSkuIds = SkuInfoListClass()

    SkuInfoList = []
    
    XmlTag = "PlatformSurfaceArea/PlatformDefinitions/SkuInfo"
    List = map(LoadSkuId, XmlList(XmlFpd, XmlTag))
    SkuInfoList = List
    
    XmlTag = "PlatformSurfaceArea/PlatformDefinitions/SkuInfo/UiSkuName"
    Value = XmlElement(XmlFpd, XmlTag)
    
    XmlTag = "PlatformSurfaceArea/DynamicPcdBuildDefinitions/PcdBuildData/SkuInfo"
    # here return a List
    List = map(LoadPlatformSkuInfo, XmlList(XmlFpd, XmlTag))

    for SkuInfo in List:
        SkuId = SkuInfo[0]
        Value = SkuInfo[1]

        SkuInfoList.append(SkuInfo)

    PlatformSkuIds.SkuInfoList = SkuInfoList

    return PlatformSkuIds
      
## Load Platform ModuleSaBuildOptions.
#
# Read an input Platform XML DOM object and return Platform ModuleSaBuildOptions class object
# contained in the DOM object.
#
# @param  XmlModuleSaBuildOptions             An XML DOM object read from FPD file.
#
# @retvel   PlatformBuildOptions               A list of Platform ModuleSaBuildOption object loaded from XmlFpd.
#
def LoadPlatformModuleSaBuildOption(XmlModuleSA):
    PlatformModuleSaBuildOption = PlatformBuildOptionClasses()
    
    XmlTag = "ModuleSA/ModuleSaBuildOptions/FvBinding"
    PlatformModuleSaBuildOption.FvBinding = XmlElement(XmlModuleSA, XmlTag)
    
    XmlTag = "ModuleSA/ModuleSaBuildOptions/FfsFormatKey"
    PlatformModuleSaBuildOption.FfsFormatKey = XmlElement(XmlModuleSA, XmlTag)
    
    XmlTag = "ModuleSA/ModuleSaBuildOptions/FfsFileNameGuid"
    FfsFileNameGuid = XmlElement(XmlModuleSA, XmlTag)
    
    #XmlTag = "ModuleSA/ModuleSaBuildOptions/Options/Option"
    #Options = map(LoadModuleSaBuildOption, XmlList(XmlModuleSA, XmlTag))
    #Options = LoadBuildOptions(XmlModuleSA)
    #PlatformModuleSaBuildOption.append(Options)
    
    return PlatformModuleSaBuildOption

## Load a list of Platform Library Classes.
#
# Read an input Platform XML DOM object and return a list of Library Classes
# contained in the DOM object.
#
# @param  XmlLibraryInstance       An XML DOM object read from FPD file.
#
# @retvel  LibraryInstance         A Library Instance loaded from XmlFpd.
#
def LoadPlatformModuleLibraryInstance(XmlLibraryInstance):
    LibraryInstance = []

    XmlTag = "ModuleGuid"
    ModuleGuid = XmlAttribute(XmlLibraryInstance, XmlTag)
    ModulePath = gEdkIIWorkspaceGuidsInfo.ResolveModuleFilePath(ModuleGuid)
    #LibraryInstance.append(ModuleGuid)
    #LibraryInstance.append(ModulePath)
    ModuleMSAFile = ModulePath.replace('.inf', '.msa')
    #ModuleMSAFileName = 'C:/SourceTree/R9/' + ModuleMSAFile
    ModuleMSAFileName = options.workspace + ModuleMSAFile
    XmlMsa = XmlParseFile(ModuleMSAFileName)
    
    XmlTag = "ModuleSurfaceArea/LibraryClassDefinitions/LibraryClass/Keyword"
    Name = XmlElement(XmlMsa, XmlTag)
    LibraryInstance.append(Name)
    LibraryInstance.append(ModulePath)
    
    #XmlTag = "PackageGuid"
    #PackageGuid = XmlAttribute(XmlLibraryInstance, XmlTag)
    #LibraryInstance.append(PackageGuid)
    return LibraryInstance

def LoadLibraryClass(XmlLibraryClass):
    XmlTag = "Usage"
    Usage = XmlAttribute(XmlLibraryClass, XmlTag)
    if Usage == "ALWAYS_PRODUCED":
        XmlTag = "SupModuleList"
        SupModuleList = XmlAttribute(XmlLibraryClass, XmlTag).split()
        return SupModuleList
        
    #List = []
    #List.append(Usage)
    
    #XmlTag = "SupModuleList"
    #SupModuleList = XmlAttribute(XmlLibraryClass, XmlTag).split()
    #List.append(SupModuleList)
    #return List

## Load Platform Library Class.
#
# Read an input Platform XML DOM object and return Platform module class object
# contained in the DOM object.
#
# @param    XmlLibraries             An XML DOM object read from FPD file.
#
# @retvel   PlatformLibraryClass     A Platform Library Class object loaded from XmlFpd.
#
def LoadPlatformLibraryClass(XmlPlatformLibraryClass):
    PlatformLibraryInstance = PlatformLibraryClass()

    XmlTag = "ModuleGuid"
    LibraryInstanceModuleGuid = XmlAttribute(XmlPlatformLibraryClass, XmlTag)
    
    XmlTag = "PackageGuid"
    LibraryInstancePackageGuid = XmlAttribute(XmlPlatformLibraryClass, XmlTag)
    
    LibraryInstancePath = gEdkIIWorkspaceGuidsInfo.ResolveModuleFilePath(LibraryInstanceModuleGuid)
    
    if LibraryInstancePath != "": # if LibraryInstancePath == "" that's because the module guid cannot be resolved
        PlatformLibraryInstance.FilePath = LibraryInstancePath
        #
        LibraryInstanceMSAName = LibraryInstancePath.replace('.inf', '.msa')
        #LibraryInstanceMSAPath = 'C:/SourceTree/R9/' + LibraryInstanceMSAName
        LibraryInstanceMSAPath = options.workspace + LibraryInstanceMSAName
    
        PlatformLibraryInstance.FilePath = LibraryInstancePath
    
        XmlMsa = XmlParseFile(LibraryInstanceMSAPath)

        XmlTag = "ModuleSurfaceArea/MsaHeader/ModuleName"
        PlatformLibraryInstance.Name = XmlElement(XmlMsa, XmlTag)
    
        XmlTag = "ModuleSurfaceArea/MsaHeader/ModuleType"
        PlatformLibraryInstance.ModuleType = XmlElement(XmlMsa, XmlTag)
    
        if PlatformLibraryInstance.ModuleType != "BASE":
            XmlTag = "ModuleSurfaceArea/LibraryClassDefinitions/LibraryClass"
            #LoadLibraryClass(PlatformLibraryInstance, XmlList(XmlMsa, XmlTag))
            
            List = map(LoadLibraryClass, XmlList(XmlMsa, XmlTag))
            PlatformLibraryInstance.SupModuleList = List[0]
        XmlTag = "ModuleSurfaceArea/ModuleDefinitions/SupportedArchitectures"
        PlatformLibraryInstance.SupArchList = XmlElement(XmlMsa, XmlTag).split()
    
        PlatformLibraryInstance.ModuleGuid = LibraryInstanceModuleGuid
    
        XmlTag = "ModuleSurfaceArea/MsaHeader/Version"
        PlatformLibraryInstance.ModuleVersion = XmlElement(XmlMsa, XmlTag)
    
        PlatformLibraryInstance.PackageGuid = LibraryInstancePackageGuid
        PlatformLibraryInstance.PackageVersion = ''
    
        return PlatformLibraryInstance

## Load Platform Library Classes.
#
# Read an input Platform XML DOM object and return Platform module class object
# contained in the DOM object.
#
# @param    XmlLibraries             An XML DOM object read from FPD file.
#
# @retvel   PlatformLibraryClasses    A list of Platform Library Class object loaded from XmlFpd.
#
def LoadPlatformLibraryClasses(XmlFpd):
    PlatformLibraryInstances = PlatformLibraryClasses()
    PlatformLibraryInstances.LibraryList = []

    List = []
    XmlTag = "PlatformSurfaceArea/FrameworkModules/ModuleSA/Libraries/Instance"
    List = map(LoadPlatformLibraryClass, XmlList(XmlFpd, XmlTag))
    #List.sort()
    PlatformLibraryInstances.LibraryList = List
    
    return PlatformLibraryInstances

## Load Platform module.
#
# Read an input Platform XML DOM object and return Platform module class object
# contained in the DOM object.
#
# @param  XmlModuleSA             An XML DOM object read from FPD file.
#
# @retvel   PlatformModule         A Platform module object loaded from XmlFpd.
#
def LoadModuleSA(XmlModuleSA):
    PlatformModule = PlatformModuleClass()

    # three parts: Libraries instances, PcdBuildDefinition, ModuleSaBuildOptions
    XmlTag = "ModuleSA/Libraries/Instance"

    PlatformModule.LibraryClasses = map(LoadPlatformModuleLibraryInstance, XmlList(XmlModuleSA, XmlTag))

    XmlTag = "ModuleSA/PcdBuildDefinition/PcdData"
    PlatformModule.PcdBuildDefinitions = map(LoadPlatformPcdData, XmlList(XmlModuleSA, XmlTag)) #bugbug fix me

    XmlTag = "ModuleSA/ModuleSaBuildOptions"
    PlatformModule.ModuleSaBuildOption = LoadPlatformModuleSaBuildOption(XmlModuleSA) #bugbug fix me

    XmlTag = "SupArchList"
    PlatformModule.SupArchList = XmlAttribute(XmlModuleSA, XmlTag).split()
    
    # the package guid which the module depends on, do not care for now
    XmlTag = "PackageGuid"
    PlatformModule.PackageGuid = XmlAttribute(XmlModuleSA, XmlTag)

    # the module guid, use this guid to get the module *.msa file and convert it to *.inf file with path
    XmlTag = "ModuleGuid"
    PlatformModule.ModuleGuid = XmlAttribute(XmlModuleSA, XmlTag)
    # use this guid to find the *.msa file path or FilePath $(WORKSPACE)/EdkModulePkg/Core/Dxe/DxeMain.msa
    # then convert $(WORKSPACE)/EdkModulePkg/Core/Dxe/DxeMain.msa to $(WORKSPACE)/EdkModulePkg/Core/Dxe/DxeMain.inf, it's FilePath
    PlatformModulePath = gEdkIIWorkspaceGuidsInfo.ResolveModuleFilePath(PlatformModule.ModuleGuid)

    PlatformModule.FilePath = PlatformModulePath # *.inf file path
    # *.inf back to *.msa
    ModuleMSAFileName = PlatformModulePath.replace('.inf', '.msa')
    #ModuleMSAFileName = 'C:/SourceTree/R9/' + ModuleMSAFileName
    ModuleMSAFileName = options.workspace + ModuleMSAFileName
    # Open this module
    #ModuleMSA = open(ModuleMSAFileName, "r")
    XmlMsa = XmlParseFile(ModuleMSAFileName)

    XmlTag = "ModuleSurfaceArea/MsaHeader/ModuleName"
    PlatformModule.Name = XmlElement(XmlMsa, XmlTag)     # ModuleName

    XmlTag = "ModuleSurfaceArea/MsaHeader/ModuleType"
    PlatformModule.ModuleType = XmlElement(XmlMsa, XmlTag)

    # IA32, X64, IPF and EBC which the module support arch
    #XmlTag = "ModuleSurfaceArea/ModuleDefinitions/SupportedArchitectures"
    #PlatformModule.SupArchList = XmlElement(XmlMsa, XmlTag).split()

    #XmlTag = "ModuleSurfaceArea/MsaHeader/"
    PlatformModule.Type = ''     #LIBRARY | LIBRARY_CLASS | MODULE, used by dsc. New in DSC spec

    PlatformModule.ExecFilePath = '' # New in DSC spec

    XmlTag = "ModuleSurfaceArea/MsaHeader/Specification"
    PlatformModule.Specifications = XmlElement(XmlMsa, XmlTag).split()

    return PlatformModule

## Load Platform modules.
#
# Read an input Platform XML DOM object and return a list of Platform modules class object
# contained in the DOM object.
#
# @param  XmlFpd                  An XML DOM object read from FPD file.
#
# @retvel   PlatformModules         A list of Platform modules object loaded from XmlFpd.
#
def LoadPlatformModules(XmlFpd):
    PlatformModules = PlatformModuleClasses()
    
    XmlTag = "PlatformSurfaceArea/FrameworkModules/ModuleSA"
    PlatformModules.ModuleList = map(LoadModuleSA, XmlList(XmlFpd, XmlTag))
    
    return PlatformModules

## Load Platform Flash Definition File.
#
# Read an input Platform XML DOM object and return Platform Flash Definition File class object
# contained in the DOM object.
#
# @param  XmlFpd                  An XML DOM object read from FPD file.
# @param  FpdFileName          The file path of FPD File.
#
# @retvel   PlatformFlashDefinitionFile         A new Platform Flash Definition File object loaded from XmlFpd.
#
def LoadPlatformFlashDefinitionFile(XmlFpd, FpdFileName):
    PlatformFlashDefinitionFile = PlatformFlashDefinitionFileClass()
    
    XmlTag = "PlatformSurfaceArea/Flash/FlashDefinitionFile"
    PlatformFlashDefinitionFile.FilePath = XmlElement(XmlFpd, XmlTag)
    PlatformFlashDefinitionFile.Id = ''
    PlatformFlashDefinitionFile.UiName = ''
    PlatformFlashDefinitionFile.Preferred = ''
    
    return PlatformFlashDefinitionFile

## Load Platform User Defined Ant Tasks.
#
# Read an input Platform XML DOM object and return platform
# User Defined Ant Tasks contained in the DOM object.
#
# @param  XmlUserDefinedAntTasks   An XML DOM object read from FPD file.
#
# @retvel  AntTask         An Ant Task loaded from XmlFpd.
#
def LoadAntTask(XmlAntTask):
    XmlTag = ""
    AntTask = []
    return AntTask

## Load Platform User Defined Ant Tasks.
#
# Read an input Platform XML DOM object and return platform
# User Defined Ant Tasks contained in the DOM object.
#
# @param  XmlUserDefinedAntTasks   An XML DOM object read from FPD file.
#
# @retvel  AntTask         An Ant Task loaded from XmlFpd.
#
def LoadUserDefinedAntTasks(XmlUserDefinedAntTasks):
    AntTask = PlatformAntTaskClass()
    
    AntTask.Id = ''
    AntTask.AntCmdOptions = ''
    AntTask.FilePath = ''
    #XmlTag = "minOccurs"
    #AntTask = XmlAttribute(XmlUserDefinedAntTasks, XmlTag)
    return AntTask

## Load Platform Build Options.
#
# Read an input Platform XML DOM object and return a list of platform
# Build Option contained in the DOM object.
#
# @param  XmlBuildOptions               An XML DOM object read from FPD file.
#
# @retvel  PlatformBuildOptions         A list of platform Build Options loaded from XmlFpd.
#
def LoadBuildOptions(XmlBuildOptions):
    XmlTag = "Option"
    return map(LoadBuildOption, XmlList(XmlBuildOptions, XmlTag)) # LoadBuildOption is a method in MigrationUtilities.py

## Load Platform Build Option.
#
# Read an input Platform XML DOM object and return a Build Option
# contained in the DOM object.
#
# @param  XmlFpd               An XML DOM object read from FPD file.
#
# @retvel  PlatformBuildOption         A Build Options loaded from XmlFpd.
#
def LoadPlatformBuildOption(XmlBuildOptions):
    PlatformBuildOption = PlatformBuildOptionClass()
    
    # handle UserDefinedAntTasks
    XmlTag = "PlatformSurfaceArea/BuildOptions/UserDefinedAntTasks/AntTask"
    PlatformBuildOption.UserDefinedAntTasks = LoadUserDefinedAntTasks(XmlTag)
    
    # handle Options
    XmlTag = "PlatformSurfaceArea/BuildOptions/Options/Option"
    PlatformBuildOption.Options = map(LoadBuildOption, XmlList(XmlBuildOptions, XmlTag))
    
    
    # handle UserExtensions
    XmlTag = "PlatformSurfaceArea/BuildOptions/UserExtensions"
    PlatformBuildOption.UserExtensions = LoadUserExtensions(XmlTag) # from MigrationUtilities.py LoadUserExtensions

    # handle Ffs
    XmlTag = "Ffs/FfsKey"
    PlatformBuildOption.FfsKeyList = map(LoadPlatformFfsKey, XmlList(XmlBuildOptions, XmlTag))

    return PlatformBuildOption

## Load a list of Platform Build Options.
#
# Read an input Platform XML DOM object and return a list of Build Options
# contained in the DOM object.
#
# @param  XmlFfs               An XML DOM object read from FPD file.
#
# @retvel  PlatformFfsKey      A platform Ffs key loaded from XmlFpd.
#
def LoadPlatformFfsKey(XmlFfs):
    PlatformFfsKey = []
    
    XmlTag = "FfsKey"
    PlatformFfsKey.Key = XmlAttribute(XmlFfs, XmlTag)

    XmlTag = "Attribute"
    for XmlAttribute in XmlList(XmlFfs, XmlTag):
        XmlTag = "Name"
        PlatformFfsKey.Name = XmlAttribute(XmlAttribute, XmlTag)
        XmlTag = "Value"
        PlatformFfsKey.Name = XmlAttribute(XmlAttribute, XmlTag)

    XmlTag = "Ffs/Sections"
    for XmlSections in XmlList(XmlFfs, XmlTag):
        XmlTag = "EncapsulationType"
        #PlatformFfsKey.EncapsulationType = XmlAttribute(XmlSections, XmlTag)

    XmlTag = "Ffs/Sections/Section"
    for XmlSection in XmlList(XmlFfs, XmlTag):
        XmlTag = "SectionType"
        #PlatformFfsKey.SectionType = XmlAttribute(XmlFfs, XmlTag)
        
    return PlatformFfsKey

## Load a list of Platform Build Options.
#
# Read an input Platform XML DOM object and return a list of Build Options
# contained in the DOM object.
#
# @param  XmlFpd               An XML DOM object read from FPD file.
#
# @retvel  PlatformBuildOptions         A list of Build Options loaded from XmlFpd.
#
def LoadPlatformBuildOptions(XmlFpd):
    XmlTag = "PlatformSurfaceArea/BuildOptions/Ffs"
    return map(LoadPlatformBuildOption, XmlList(XmlFpd, XmlTag))

## Load Platform Pcd Data.
#
# Read an input Platform XML DOM object and return Platform module class object
# contained in the DOM object.
#
# @param    XmlPcd             An XML DOM object read from FPD file.
#
# @retvel   PlatformPcdData    A Platform Pcd object loaded from XmlFpd.
#
def LoadPlatformPcdData(XmlPcdData):
    PcdData = PcdClass() # defined in CommonDataClass.CommonClass.py

    XmlTag = "ItemType"
    PcdData.ItemType = XmlAttribute(XmlPcdData, XmlTag) #DYNAMIC

    XmlTag = "PcdData/C_Name"
    PcdData.C_NAME = XmlElement(XmlPcdData, XmlTag)
    
    XmlTag = "PcdData/Token"
    PcdData.Token = XmlElement(XmlPcdData, XmlTag)
    
    XmlTag = "PcdData/TokenSpaceGuidCName"
    PcdData.TokenSpaceGuidCName = XmlElement(XmlPcdData, XmlTag)
    
    XmlTag = "PcdData/DatumType"
    PcdData.DatumType = XmlElement(XmlPcdData, XmlTag)
    
    XmlTag = "PcdData/MaxDatumSize"
    PcdData.MaxDatumSize = XmlElement(XmlPcdData, XmlTag)
    
    #XmlTag = "PcdData/Value"
    #PcdData.Value = XmlElement(XmlPcdData, XmlTag)
    
    return PcdData

## Load a Platform Pcd Build Data.
#
# Read an input Platform XML DOM object and return a list of Pcd Dynamic
# contained in the DOM object.
#
# @param  XmlPcdBuildData        An XML DOM object read from FPD file.
#
# @retvel   PcdBuildData         A Platform Pcd Build Data loaded from XmlFpd.
#
def LoadPlatformPcdBuildData(XmlPcdBuildData):
    PcdBuildData = PcdClass() # defined in CommonDataClass.CommonClass.py

    XmlTag = "ItemType"
    PcdBuildData.ItemType = XmlAttribute(XmlPcdBuildData, XmlTag) #DYNAMIC

    XmlTag = "PcdBuildData/C_Name"
    PcdBuildData.C_NAME = XmlElement(XmlPcdBuildData, XmlTag)

    XmlTag = "PcdBuildData/Token"
    PcdBuildData.Token = XmlElement(XmlPcdBuildData, XmlTag)

    XmlTag = "PcdBuildData/TokenSpaceGuidCName"
    PcdBuildData.TokenSpaceGuidCName = XmlElement(XmlPcdBuildData, XmlTag)

    XmlTag = "PcdBuildData/DatumType"
    PcdBuildData.DatumType = XmlElement(XmlPcdBuildData, XmlTag)

    XmlTag = "PcdBuildData/MaxDatumSize"
    PcdBuildData.MaxDatumSize = XmlElement(XmlPcdBuildData, XmlTag)

    return PcdBuildData

## Load a list of Platform Pcd Dynamic.
#
# Read an input Platform XML DOM object and return a list of Pcd Dynamic
# contained in the DOM object.
#
# @param  XmlFpd               An XML DOM object read from FPD file.
#
# @retvel   PcdDynamic         A list of Pcd Dynamic loaded from XmlFpd.
#
def LoadDynamicPcdBuildDefinitions(XmlFpd):
    DynamicPcdBuildDefinitions = []
    XmlTag = "PlatformSurfaceArea/DynamicPcdBuildDefinitions/PcdBuildData"
    return map(LoadPlatformPcdBuildData, XmlList(XmlFpd, XmlTag))

## Load a Platform Fv Image Name object.
#
# Read an input Platform XML DOM object and return a platform Fv Image
# Name contained in the DOM object.
#
# @param  XmlFvImageNames     An XML DOM object read from FPD file.
#
# @retvel FvImageName          A Platform Fv Image Name object
#
def LoadFvImageName(XmlFvImageNames):
    XmlTag = "FvImageNames"
    FvImageName = XmlElement(XmlFvImageNames, XmlTag)
    return FvImageName

## Load a Platform Fv Image option object.
#
# Read an input Platform XML DOM object and return a platform Fv Image
# Option contained in the DOM object.
#
# @param  XmlFvImageOptions     An XML DOM object read from FPD file.
#
# @retvel FvImageOption          A Platform Fv Image Option object
#
def LoadFvImageOption(XmlFvImageOptions):
    XmlTag = "NameValue"
    FvImageOption = XmlElement(XmlFvImageOptions, XmlTag)
    return FvImageOption

## Load a Platform Fv Image object.
#
# Read an input Platform XML DOM object and return a platform Fv Image
# contained in the DOM object.
#
# @param  XmlFvImage       An XML DOM object read from FPD file.
#
# @retvel FvImage          A Platform Fv Image object
#
def LoadFvImage(XmlFvImage):
    FvImage = PlatformFvImageClass()

    XmlTag = ""
    FvImage.Name = ''
    
    XmlTag = ""
    FvImage.Value = ''
    
    XmlTag = "Type"
    FvImage.Type = XmlAttribute(XmlFvImage, XmlTag)
    
    XmlTag = "FvImage/FvImageNames"
    FvImage.FvImageNames = map(LoadFvImageName, XmlList(XmlFvImage, XmlTag))
    
    XmlTag = "FvImage/FvImageOptions"
    FvImage.FvImageOptions = map(LoadFvImageOption, XmlList(XmlFvImage, XmlTag))
    
    return FvImage

## Load a Platform NameValue object.
#
# Read an input Platform XML DOM object and return a list of User Extensions
# contained in the DOM object.
#
# @param  XmlNameValue       An XML DOM object read from FPD file.
#
# @retvel NameValue          A Platform NameValue object
#
def LoadNameValue(XmlNameValue):
    NameValue = []
    
    XmlTag = "Name"
    Name = XmlAttribute(XmlNameValue, XmlTag)
    NameValue.append(Name)

    XmlTag = "Value"
    Value = XmlAttribute(XmlNameValue, XmlTag)
    NameValue.append(Value)
    
    return NameValue

## Load a Platform fdf object.
#
# Read an input Platform XML DOM object and return a list of User Extensions
# contained in the DOM object.
#
# @param  XmlFvImages          An XML DOM object read from FPD file.
#
# @retvel PlatformFdf          A Platform fdf object
#
def LoadPlatformFdf(XmlFvImages):
    #PlatformFdf = FdfClassObject()
    PlatformFdf = []
    # PlatformFds is a list of platform Fdfs [Fdf,....]
    # PlatformFdf [FV,...]
    # [FV] is a list of [Ffs]
    #[[Fdf],...]
    #[[[FV],...],...]
    #[[[Ffs,...],...],...]
    PlatformFfs = PlatformFfsClass()
    
    PlatformFvImageName = PlatformFvImageNameClass()
    #XmlTag = "FvImages/NameValue/Name"
    XmlTag = "FvImages/NameValue"
    List = []
    List = map(LoadNameValue, XmlList(XmlFvImages, XmlTag))
    
    #PlatformFvImageName.Name = XmlAttribute(XmlFvImages, XmlTag)
    
    #XmlTag = "FvImages/NameValue/Value"
    #PlatformFvImageName.Value = XmlAttribute(XmlFvImages, XmlTag)
    PlatformFdf.append(List)
    
    PlatformFvImages = PlatformFvImagesClass()
    XmlTag = "FvImages/FvImage"
    List = []
    PlatformFvImages.FvImages = [] # list of FvImage
    List = map(LoadFvImage, XmlList(XmlFvImages, XmlTag))
    PlatformFvImages.FvImages = List
    PlatformFdf.append(PlatformFvImages)
    
    
    #PlatformFvImage = PlatformFvImageClass()
    #PlatformFvImage.Name = ''
    #PlatformFvImage.Value = ''
    #PlatformFvImage.Type = ''
    #PlatformFvImage.FvImageNames = []
    #PlatformFvImage.FvImageOptions = []
    
    PlatformFfs.Attribute = () #{ [(Name, PlatformFfsSectionsClass)] : Value}
    PlatformFfs.Sections = [] #[ PlatformFfsSectionsClass]
    
    PlatformFfsSections = PlatformFfsSectionsClass()
    PlatformFfsSections.BindingOrder = ''
    PlatformFfsSections.Compressible = ''
    PlatformFfsSections.SectionType = ''
    PlatformFfsSections.EncapsulationType = ''
    PlatformFfsSections.ToolName = ''
    PlatformFfsSections.Section = [] #[ PlatformFfsSectionClass, ... ]
    PlatformFfsSections.Sections = [] #[ PlatformFfsSectionsClass, ...]
    
    
    PlatformFfsSection = PlatformFfsSectionClass()
    PlatformFfsSection.BindingOrder = ''
    PlatformFfsSection.Compressible = ''
    PlatformFfsSection.SectionType = ''
    PlatformFfsSection.EncapsulationType = ''
    PlatformFfsSection.ToolName = ''
    PlatformFfsSection.Filenames = []
    PlatformFfsSection.Args = ''
    PlatformFfsSection.OutFile = ''
    PlatformFfsSection.OutputFileExtension = ''
    PlatformFfsSection.ToolNameElement = ''
    
    #PlatformFvImages = PlatformFvImagesClass()
    #PlatformFvImages.FvImages1 = []
    #PlatformFvImages.FvImages2 = []
    
    #PlatformFvImageName = PlatformFvImageNameClass()
    #PlatformFvImageName.Name = ''
    #PlatformFvImageName.Type = '' #FV_MAIN | FV_MAIN_COMPACT | NV_STORAGE | FV_RECOVERY | FV_RECOVERY_FLOPPY | FV_FILE | CAPSULE_CARGO | NULL | USER_DEFINED
    #PlatformFvImageName.FvImageOptions = [] #[ PlatformFvImageOption, ...]
    
    #PlatformFvImage = PlatformFvImageClass()
    #PlatformFvImage.Name = ''
    #PlatformFvImage.Type = '' #Attributes | Options | Components | ImageName
    #PlatformFvImage.Value = ''
    #PlatformFvImage.FvImageNames = []
    #PlatformFvImage.FvImageOptions = [] #[ PlatformFvImageOption, ...]

    #PlatformFvImageOption = PlatformFvImageOptionClass()
    #PlatformFvImageOption.FvImageOptionName = ''
    #PlatformFvImageOption.FvImageOptionValues = []
    
    return PlatformFdf

## Load a list of Platform fdf objects.
#
# Read an input Platform XML DOM object and return a list of User Extensions
# contained in the DOM object.
#
# @param  XmlFpd               An XML DOM object read from FPD file.
#
# @retvel PlatformFdfs          A list of Platform fdf object
#
def LoadPlatformFdfs(XmlFpd):
    XmlTag = "PlatformSurfaceArea/Flash/FvImages"
    PlatformFdfs = map(LoadPlatformFdf, XmlList(XmlFpd, XmlTag))
    return PlatformFdfs

## Load a Platform User Extensions.
#
# Read an input Platform XML DOM object and return an User Extension
# contained in the DOM object.
#
# @param  XmlUserExtension    An XML DOM object read from FPD file.
#
# @retvel PlatformUserExtensions       A platform User Extension loaded from XmlFpd
#
def LoadPlatformUserExtension(XmlUserExtension):
    PlatformUserExtensions = UserExtensionsClass()

    XmlTag = "UserID"
    PlatformUserExtensions.UserID = XmlAttribute(XmlUserExtension, XmlTag)
    
    XmlTag = "Identifier"
    PlatformUserExtensions.Identifier = XmlAttribute(XmlUserExtension, XmlTag)
    
    PlatformUserExtensions.Content = XmlElementData(XmlUserExtension)
    
    return PlatformUserExtensions

## Load a list of Platform User Extensions.
#
# Read an input Platform XML DOM object and return a list of User Extensions
# contained in the DOM object.
#
# @param  XmlFpd               An XML DOM object read from FPD file.
#
# @retvel UserExtensions       A list of platform User Extensions loaded from XmlFpd
#
def LoadPlatformUserExtensions(XmlFpd):
    PlatformUserExtensions = []

    XmlTag = "PlatformSurfaceArea/UserExtensions"
    return map(LoadPlatformUserExtension, XmlList(XmlFpd, XmlTag)) # from MigrationUtilities.py LoadUserExtensions

## Load a new Platform class object.
#
# Read an input FPD File and return a new Platform class Object.
#
# @param  FpdFileName          An XML DOM object read from FPD file.
#
# @retvel  Platform                 A new Platform class object loaded from FPD File.
#
def LoadFpd(FpdFileName):
    XmlFpd = XmlParseFile(FpdFileName)
    EdkLogger.verbose("Load FPD File: %s" % FpdFileName)
    
    Platform = PlatformClass()
    Platform.Header = LoadPlatformHeader(XmlFpd, FpdFileName)
    Platform.SkuInfos = LoadPlatformSkuInfos(XmlFpd)
    Platform.Libraries = [] #New in dsc spec, do not handle for now
    Platform.LibraryClasses = LoadPlatformLibraryClasses(XmlFpd)
    Platform.Modules = LoadPlatformModules(XmlFpd)
    Platform.FlashDefinitionFile = LoadPlatformFlashDefinitionFile(XmlFpd, FpdFileName)
    Platform.BuildOptions = LoadPlatformBuildOptions(XmlFpd)
    Platform.DynamicPcdBuildDefinitions = LoadDynamicPcdBuildDefinitions(XmlFpd)
    Platform.Fdf = LoadPlatformFdfs(XmlFpd)
    Platform.UserExtensions = LoadPlatformUserExtensions(XmlFpd)

    return Platform

# This acts like the main() function for the script, unless it is 'import'ed
# into another script.
if __name__ == '__main__':
    pass