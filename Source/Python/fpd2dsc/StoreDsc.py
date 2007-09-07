## @file
# Store a Module class object to an INF file.
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
from LoadFpd import LoadFpd
from CommonDataClass.PlatformClass import *
from CommonDataClass.FdfClassObject import *
from Common.MigrationUtilities import *
from Common.ToolDefClassObject import *
from Common.TargetTxtClassObject import *

## Store Defines section.
#
# Write [Defines] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                 The output DSC file to store the Defines section.
# @param  Platform               An input Platform class object.
#
def StorePlatformDefinesSection(DscFile, Platform):
    PlatformHeader = Platform.Header
    
    DefinesTupleList = []
    
    if PlatformHeader.Name != "":
        DefinesTupleList.append(("PLATFORM_NAME", PlatformHeader.Name))

    if PlatformHeader.Guid != "":
        DefinesTupleList.append(("PLATFORM_GUID", PlatformHeader.Guid))

    if PlatformHeader.Version != "":
        DefinesTupleList.append(("PLATFORM_VERSION", PlatformHeader.Version))

    DefinesTupleList.append(("DSC_ SPECIFICATION", PlatformHeader.DscSpecification))
    
    if PlatformHeader.OutputDirectory != "":
        DefinesTupleList.append(("OUTPUT_DIRECTORY", PlatformHeader.OutputDirectory))

    if PlatformHeader.SupArchList != "":
        String = "|".join(PlatformHeader.SupArchList)
        DefinesTupleList.append(("SUPPORTED_ARCHITECTURES", String))

    if PlatformHeader.BuildTargets != "":
        String = "|".join(PlatformHeader.BuildTargets)
        DefinesTupleList.append(("BUILD_TARGETS", String))

    if PlatformHeader.SkuIdName != "":
        #DefinesTupleList.append(("SKUID_IDENTIFIER", PlatformHeader.SkuIdName))
        String = "|".join(PlatformHeader.SkuIdName)
        DefinesTupleList.append(("SKUID_IDENTIFIER", String))
        
	String = Platform.FlashDefinitionFile.FilePath
	DefinesTupleList.append(("FLASH_DEFINITION", String))
	
    StoreDefinesSection(DscFile, DefinesTupleList)

## Store SkuIds section.
#
# Write [SkuIds] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                 The output DSC file to store the Library Classes section.
# @param  Platform               An input Platform class object.
#
def StorePlatformSkuIdsSection(DscFile, Platform):
    Section = "[SkuIds]" + '\n'
    
    List = Platform.SkuInfos.SkuInfoList
    for Item in List:
        Section = Section + "%s" % Item[0] + '|' + "%s" % Item[1] + '\n'
    Section = Section + '\n'
    
    StoreTextFile(DscFile, Section)

## Return a Build Option Item.
#
# Read the input LibraryClass class object and return Platform Build Option Item.
#
# @param  Item         An Specified CPU Arch object.
# @param  Dict1        An input Dictionary containing the build option information.
#
# @retval Section     A Platform Build Option Section Item.
#
def GetBuildOption(Item, Dict1):
    Section = "[BuildOptions." + Item + "]\n"
    for key in Dict1.keys():
        if key.find(Item + "_CC_FLAGS") != -1:
            if key.find('WINDDK3790x1830') != -1:
                b = Dict1.get(key)
                Section += "*_WINDDK3790x1830_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('VS2003') != -1:
                b = Dict1.get(key)
                Section += "*_VS2003_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('VS2005EXP') != -1:
                b = Dict1.get(key)
                Section += "*_VS2005EXP_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('VS2005STD') != -1:
                b = Dict1.get(key)
                Section += "*_VS2005STD_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('VS2005PRO') != -1:
                b = Dict1.get(key)
                Section += "*_VS2005PRO_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('VS2005TEAMSUITE') != -1:
                b = Dict1.get(key)
                Section += "*_VS2005TEAMSUITE_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('UNIXGCC') != -1:
                b = Dict1.get(key)
                Section += "*_UNIXGCC_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('CYGWINGCC') != -1:
                b = Dict1.get(key)
                Section += "*_CYGWINGCC_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('ELFGCC') != -1:
                b = Dict1.get(key)
                Section += "*_ELFGCC_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('ICC') != -1:
                a = Dict1.get(key).split(' ')
                Section += "*_ICC_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            elif key.find('MYTOOLS') != -1:
                a = Dict1.get(key).split(' ')
                Section += "*_MYTOOLS_" + Item + "_CC_FLAGS" + "  =  " + b + "\n"
            else:
                print "Error!"
    return Section

## Store Build Options section.
#
# Write [BuildOptions] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                 The output DSC file to store the Build Options section.
# @param  Platform               An input Platform class object.
#
def StorePlatformBuildOptionsSection(DscFile, Platform):
    # which is from tools_def.txt
    StandardBuildTargets = ["DEBUG", "RELEASE"]
    SupportedArches = ["COMMON", "IA32", "X64", "IPF", "EBC"]
    Target = TargetTxtClassObject()
    workspace = os.getenv('WORKSPACE')
    Target.LoadTargetTxtFile(workspace + '\\Conf\\target.txt')
    ToolDef = ToolDefClassObject()
    ToolDef.LoadToolDefFile(workspace + '\\' + Target.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF])
    # Now we have got ToolDef object
    #ToolDef.ToolsDefTxtDictionary
    Dict = ToolDef.ToolsDefTxtDatabase

    Dict1 = ToolDef.ToolsDefTxtDictionary # we care the info in this Dict
    #
    # We only support *(DEBUG/RELEASE) and *(All Arch: IA32, X64, IPF and EBC) for now
    #
    #
    # First need to check which arch
    #
    Archs = Platform.Header.SupArchList
    BuildTargets = Platform.Header.BuildTargets
    if BuildTargets == StandardBuildTargets:
        print "Debug and Release both support" # skip debug/release string search
    else:
        print "need to search debug/release string"

    if len(Archs) == 4:
        print "support all Arch, skip search Arch"
    else:
        for Item in Archs:
            if Item == 'IA32':
                Section = GetBuildOption(Item, Dict1)
            elif Item == 'X64':
                Section = GetBuildOption(Item, Dict1)
            elif Item == 'IPF':
                Section = GetBuildOption(Item, Dict1)
            elif Item == 'EBC':
                Section = GetBuildOption(Item, Dict1)
            else:
                print 'Error!'
        Section += "\n"
    StoreTextFile(DscFile, Section)

## Store Libraries section.
#
# Write [Libraries] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                 The output DSC file to store the Library Classes section.
# @param  Platform               An input Platform class object.
#
def StorePlatformLibrariesSection(DscFile,Platform):
    Section = '[Libraries]\n\n'
    StoreTextFile(DscFile, Section)

## Return a Platform Library Class Item.
#
# Read the input LibraryClass class object and return one line of Library Class Item.
#
# @param  LibraryClass         An input LibraryClass class object.
#
# @retval LibraryClassItem     A Module Library Class Item.
#
def GetPlatformLibraryClassItem(LibraryClass):
    LibraryClassList = []
    LibraryClassList.append(LibraryClass.Name)
    LibraryClassList.append(LibraryClass.FilePath)

    return "|".join(LibraryClassList).rstrip("|")

## Add item to a LibraryClass section.
#
# Add an Item with specific Module Type to section dictionary.
# The possible duplication is ensured to be removed.
#
# @param  Section            Section dictionary indexed by CPU architecture.
# @param  SupModuleList      LibraryClass SupModuleList: BASE, SEC, PEI_CORE, PEIM, etc.
# @param  Item               The Item to be added to section dictionary.
#
def AddToLibraryClassSection(Section, SupModuleList, Item):
    for ModuleType in SupModuleList:
        
        SectionModule = Section.get(ModuleType, [])
        if Item not in SectionModule:
            SectionModule.append(Item)
            Section[ModuleType] = SectionModule

## Get Library Classes section contents.
#
# Return the content of section named SectionName.
# the contents is based on Methods and ObjectLists.
#
# @param  SectionName        The name of the section.
# @param  Method             A function returning a string item of an object.
# @param  ObjectList         The list of object.
#
# @retval Section            The string content of a section.
#
def GetLibraryClassesSection(SectionName, Method, ObjectList):
    SupportedArches = ["COMMON", "IA32", "X64", "IPF", "EBC"]
    ModuleTypes = ["BASE","SEC","PEI_CORE","PEIM","DXE_CORE","DXE_DRIVER","DXE_SMM_DRIVER","DXE_SAL_DRIVER","DXE_RUNTIME_DRIVER","UEFI_DRIVER","UEFI_APPLICATION"]
    SectionCommonDict = {}
    SectionIA32Dict = {}
    SectionX64Dict = {}
    SectionIPFDict = {}
    SectionEBCDict = {}
    ObjectList = list(set(ObjectList)) # delete the same element in the list
    for Object in ObjectList:
        if Object == None:
            continue
        Item = Method(Object)
        if Item == "":
            continue
        Item = "  %s" % Item
        Arches = Object.SupArchList
        if len(Arches) == 4:
            ModuleType = Object.ModuleType
            # [LibraryClasses.Common.ModuleType]
            if ModuleType == "BASE":
                SupModuleList = ["BASE"]
                AddToLibraryClassSection(SectionCommonDict, SupModuleList, Item)
            else:
                #
                SupModuleList = Object.SupModuleList
                #AddToSection(SectionDict, "|".join(SupModuleList), Item)
                AddToLibraryClassSection(SectionCommonDict, SupModuleList, Item)
        else:
            # Arch
            for Arch in SupportedArches:
                if Arch.upper() in Arches:
                    if Arch == "IA32":
                        # [LibraryClasses.IA32.ModuleType]
                        ModuleType = Object.ModuleType
                        if ModuleType == "BASE":
                            SupModuleList = ["BASE"]
                            AddToLibraryClassSection(SectionIA32Dict, SupModuleList, Item)
                        else:
                            SupModuleList = Object.SupModuleList
                            AddToLibraryClassSection(SectionIA32Dict, SupModuleList, Item)
                    elif Arch == "X64":
                        # [LibraryClasses.X64.ModuleType]
                        ModuleType = Object.ModuleType
                        if ModuleType == "BASE":
                            SupModuleList = ["BASE"]
                            AddToLibraryClassSection(SectionX64Dict, SupModuleList, Item)
                        else:
                            SupModuleList = Object.SupModuleList
                            AddToLibraryClassSection(SectionX64Dict, SupModuleList, Item)
                    elif Arch == "IPF":
                        # [LibraryClasses.IPF.ModuleType]
                        ModuleType = Object.ModuleType
                        if ModuleType == "BASE":
                            SupModuleList = ["BASE"]
                            AddToLibraryClassSection(SectionIPFDict, SupModuleList, Item)
                        else:
                            SupModuleList = Object.SupModuleList
                            AddToLibraryClassSection(SectionIPFDict, SupModuleList, Item)
                    elif Arch == "EBC":
                        # [LibraryClasses.EBC.ModuleType]
                        ModuleType = Object.ModuleType
                        if ModuleType == "BASE":
                            SupModuleList = ["BASE"]
                            AddToLibraryClassSection(SectionEBCDict, SupModuleList, Item)
                        else:
                            SupModuleList = Object.SupModuleList
                            AddToLibraryClassSection(SectionEBCDict, SupModuleList, Item)

    Section = ""
    for ModuleType in ModuleTypes:
        SectionCommonModule = "\n".join(SectionCommonDict.get(ModuleType, []))
        if SectionCommonModule != "":
            Section += "[%s.Common.%s]\n%s\n" % (SectionName, ModuleType, SectionCommonModule)
            Section += "\n"
        SectionIA32Module = "\n".join(SectionIA32Dict.get(ModuleType, []))
        if SectionIA32Module != "":
            Section += "[%s.IA32.%s]\n%s\n" % (SectionName, ModuleType, SectionIA32Module)
            Section += "\n"
        SectionX64Module = "\n".join(SectionX64Dict.get(ModuleType, []))
        if SectionX64Module != "":
            Section += "[%s.X64.%s]\n%s\n" % (SectionName, ModuleType, SectionX64Module)
            Section += "\n"
        SectionIPFModule = "\n".join(SectionIPFDict.get(ModuleType, []))
        if SectionIPFModule != "":
            Section += "[%s.IPF.%s]\n%s\n" % (SectionName, ModuleType, SectionIPFModule)
            Section += "\n"
        SectionEBCModule = "\n".join(SectionEBCDict.get(ModuleType, []))
        if SectionEBCModule != "":
            Section += "[%s.EBC.%s]\n%s\n" % (SectionName, ModuleType, SectionEBCModule)
            Section += "\n"

    if Section != "":
        Section += "\n"
    return Section

## Store Library Classes section.
#
# Write [LibraryClasses] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                 The output DSC file to store the Library Classes section.
# @param  Platform               An input Platform class object.
#
def StorePlatformLibraryClassesSection(DscFile, Platform):
    Section = GetLibraryClassesSection("LibraryClasses", GetPlatformLibraryClassItem, Platform.LibraryClasses.LibraryList)
    StoreTextFile(DscFile, Section)


## Store Pcd section.
#
# Write [Pcd] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                 The output DSC file to store the Build Options section.
# @param  Platform               An input Platform class object.
#
def StorePlatformPcdSection(DscFile, Platform):
    # {PcdsFixedAtBuild:String1, PcdsFixedAtBuild:String2, PcdsPatchableInModule:String3}
    SectionDict = {}
    #
    # [PcdsFixedAtBuild], [PcdsPatchableInModule] and [PcdsFeatureFlag] are from platform.modules
    # [PcdsDynamic] is from platform.DynamicPcdBuildDefinitions
    #
    Modules = Platform.Modules.ModuleList # it's a list of modules
    for Module in Modules:
        PcdBuildDefinitions = Module.PcdBuildDefinitions # it's a list of PcdData
        for PcdData in PcdBuildDefinitions:
            List = []
            List.append(PcdData.C_NAME)
            List.append(PcdData.Token)
            List.append(PcdData.TokenSpaceGuidCName)
            List.append(PcdData.DatumType)
            List.append(PcdData.MaxDatumSize)
            String = "|".join(List)
            ItemType = PcdData.ItemType
            if PcdData.ItemType == "FIXED_AT_BUILD":
                SectionPcdsFixedAtBuild = SectionDict.get(ItemType, [])
                if String not in SectionPcdsFixedAtBuild:
                    SectionPcdsFixedAtBuild.append(String)
                    SectionDict[ItemType] = SectionPcdsFixedAtBuild
            elif PcdData.ItemType == "FEATURE_FLAG":
                SectionPcdsFeatureFlag = SectionDict.get(ItemType, [])
                if String not in SectionPcdsFeatureFlag:
                    SectionPcdsFeatureFlag.append(String)
                    SectionDict[ItemType] = SectionPcdsFeatureFlag
            elif PcdData.ItemType == "PATCHABLE_IN_MODULE":
                SectionPcdsPatchableInModule = SectionDict.get(ItemType, [])
                if String not in SectionPcdsPatchableInModule:
                    SectionPcdsPatchableInModule.append(String)
                    SectionDict[ItemType] = SectionPcdsPatchableInModule
            elif PcdData.ItemType == "DYNAMIC":
                SectionPcdsDynamic = SectionDict.get(ItemType, [])
                if String not in SectionPcdsDynamic:
                    SectionPcdsDynamic.append(String)
                    SectionDict[ItemType] = SectionPcdsDynamic
            else:
                print "Error!"
        
    DynamicPcdBuildDefinitions = Platform.DynamicPcdBuildDefinitions # It's a list
    for PcdBuildData in DynamicPcdBuildDefinitions:
        List = []
        List.append(PcdData.C_NAME)
        List.append(PcdData.Token)
        List.append(PcdData.TokenSpaceGuidCName)
        List.append(PcdData.DatumType)
        List.append(PcdData.MaxDatumSize)
        String = "|".join(List)
        if PcdBuildData.ItemType == "DYNAMIC":
            ItemType = PcdBuildData.ItemType
            SectionPcdsDynamic = SectionDict.get(ItemType, [])
            if String not in SectionPcdsDynamic:
                SectionPcdsDynamic.append(String)
                SectionDict[ItemType] = SectionPcdsDynamic
    ItemType = "FIXED_AT_BUILD"
    Section = "[PcdsFixedAtBuild]\n" + "\n".join(SectionDict.get(ItemType, []))
    ItemType = "FEATURE_FLAG"
    Section += "\n\n[PcdsFeatureFlag]\n" + "\n".join(SectionDict.get(ItemType, []))
    ItemType = "PATCHABLE_IN_MODULE"
    Section += "\n\n[PcdsPatchableInModule]\n" + "\n".join(SectionDict.get(ItemType, []))
    ItemType = "DYNAMIC"
    Section += "\n\n[PcdsDynamic]\n" + "\n".join(SectionDict.get(ItemType, []))
    Section += "\n"
    StoreTextFile(DscFile, Section)

## Return one Platform Pcd Dynamic Section.
#
# Read the input Pcd Dynamic Section class object and return one section.
#
# @param  PcdDynamic              An input PcdDynamic class object.
#
# @retval   PcdDynamicSection A section representing PcdDynamic object.
#    
def GetPlatformPcdDynamicItem(PcdDynamic):
    CName = Pcd.CName
    Token = Pcd.Token
    TokenSpaceGuidCName = Pcd.TokenSpaceGuidCName
    DatumType = Pcd.DatumType
    PcdList = [CName, Token, TokenSpaceGuidCName, DatumType]
    if Pcd.ItemType == "DYNAMIC":
        PcdList.append(Pcd.ItemType)
    
    return "|".join(PcdList)
    
## Store Pcd Dynamic section.
#
# Write [PcdDynamic] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                 The output DSC file to store the Build Options section.
# @param  Platform               An input Platform class object.
#
def StorePlatformPcdDynamicSection(DscFile, Platform):
    PcdsDict = {}
    for Pcd in Platform.PcdDeclarations:
        if Pcd.ItemType == "DYNAMIC":
            AddToPcdsDict(PcdsDict, PcdItemType, Pcd)

    Section = ""
    for PcdSectionName in PcdsDict:
        Pcds = PcdsDict[PcdSectionName]
        Section += GetSection(PcdSectionName, GetPlatformPcdDynamicItem, Pcds)
        Section += "\n"

    StoreTextFile(DscFile, Section)

## Add item to a section.
#
# Add an Item with specific CPU architecture to section dictionary.
# The possible duplication is ensured to be removed.
#
# @param  Section            Section dictionary indexed by CPU architecture.
# @param  Arch               CPU architecture: Ia32, X64, Ipf, Ebc or Common.
# @param  Item               The Item to be added to section dictionary.
#
def AddToSection(Section, Arch, Item):
    SectionArch = Section.get(Arch, [])
    if Item not in SectionArch:
        SectionArch.append(Item)
        Section[Arch] = SectionArch

## Get section contents.
#
# Return the content of section named SectionName.
# the contents is based on Methods and ObjectLists.
#
# @param  SectionName        The name of the section.
# @param  Method             A function returning a string item of an object.
# @param  ObjectList         The list of object.
#
# @retval Section            The string content of a section.
#
def GetSection(SectionName, Method, ObjectList):
    SupportedArches = ["COMMON", "IA32", "X64", "IPF", "EBC"]
    SectionDict = {}
    for Object in ObjectList:
        if Object.FilePath == "":
            continue
        Item = Method(Object)
        if Item == "":
            continue
        Item = "  %s" % Item
        Arches = Object.SupArchList
        if len(Arches) == 4:
            AddToSection(SectionDict, "common", Item)
        else:
            for Arch in SupportedArches:
                if Arch.upper() in Arches:
                    AddToSection(SectionDict, Arch, Item)

    Section = ""
    for Arch in SupportedArches:
        SectionArch = "\n".join(SectionDict.get(Arch, []))
        if SectionArch != "":
            Section += "[%s.%s]\n%s\n" % (SectionName, Arch, SectionArch)
            Section += "\n"
    if Section != "":
        Section += "\n"
    return Section

## Return a Platform Component Item.
#
# Read the input Platform Component object and return one line of Platform Component Item.
#
# @param  Component         An input Platform Component class object.
#
# @retval ComponentItem     A Platform Component Item.
#
def GetPlatformComponentItem(Component):
    List = []
    Section = {}

    List.append(Component.FilePath)

    LibraryClasses = Component.LibraryClasses
    List.append("{\n<LibraryClasses>")
    for LibraryClass in LibraryClasses:
        if LibraryClass == ["", ""]:
            continue
        List.append(LibraryClass[0] + "|" + LibraryClass[1])
    PcdBuildDefinitions = Component.PcdBuildDefinitions
    for PcdData in PcdBuildDefinitions:
        List1 = []
        List1.append(PcdData.C_NAME)
        List1.append(PcdData.Token)
        List1.append(PcdData.TokenSpaceGuidCName)
        List1.append(PcdData.DatumType)
        List1.append(PcdData.MaxDatumSize)
        String = "|".join(List1)
        ItemType = PcdData.ItemType
        if ItemType == "FIXED_AT_BUILD":
            SectionPcd = Section.get(ItemType, [])
            if String not in SectionPcd:
                SectionPcd.append(String)
            Section[ItemType] = SectionPcd
        elif ItemType == "FEATURE_FLAG":
            SectionPcd = Section.get(ItemType, [])
            if String not in SectionPcd:
                SectionPcd.append(String)
            Section[ItemType] = SectionPcd
        elif ItemType == "PATCHABLE_IN_MODULE":
            SectionPcd = Section.get(ItemType, [])
            if String not in SectionPcd:
                SectionPcd.append(String)
            Section[ItemType] = SectionPcd
        elif ItemType == "DYNAMIC":
            SectionPcd = Section.get(ItemType, [])
            if String not in SectionPcd:
                SectionPcd.append(String)
            Section[ItemType] = SectionPcd
        else:
            print "Error!"
    ItemType = "FIXED_AT_BUILD"
    if Section.get(ItemType, []) != []:
        List.append("\n<PcdsFixedAtBuild>")
        List.append("\n".join(Section.get(ItemType,[])))
    ItemType = "FEATURE_FLAG"
    if Section.get(ItemType, []) != []:
        List.append("\n<PcdsFeatureFlag>")
        List.append("\n".join(Section.get(ItemType,[])))
    ItemType = "PATCHABLE_IN_MODULE"
    if Section.get(ItemType, []) != []:
        List.append("\n<PcdsPatchableInModule>")
        List.append("\n".join(Section.get(ItemType,[])))
    ItemType = "DYNAMIC"
    if Section.get(ItemType, []) != []:
        List.append("\n<PcdsDynamic>")
        List.append("\n".join(Section.get(ItemType,[])))
    
    ModuleSaBuildOption = Component.ModuleSaBuildOption
    List.append("\n<ModuleSaBuildOption>")
    List.append(ModuleSaBuildOption.FvBinding + "|" + ModuleSaBuildOption.FfsFormatKey + "\n")
    
    return "\n".join(List)

## Store Components section.
#
# Write [Components] section to the DscFile based on Platform class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                The output DSC file to store the Components section.
# @param  Platform               An input Platform class object.
#
def StorePlatformComponentsSection(DscFile, Platform):
    Section = GetSection("Components", GetPlatformComponentItem, Platform.Modules.ModuleList)
    StoreTextFile(DscFile, Section)

## Store User Extensions section.
#
# Write [UserExtensions] section to the InfFile based on Module class object.
# Different CPU architectures are specified in the subsection if possible.
#
# @param  DscFile                The output DSC file to store the User Extensions section.
# @param  Platform               An input Platform class object.
#
def StorePlatformUserExtensionsSection(DscFile, Platform):
    Section = "".join(map(GetUserExtensions, Platform.UserExtensions))
    StoreTextFile(DscFile, Section)
    
## Store a Platform class object to a new DSC file.
#
# Read an input Platform class object and save the contents to a new DSC file.
#
# @param  DSCFileName          The output DSC file.
# @param  Platform                  An input Platform class object.
#
def StoreDsc(DscFileName, Platform):
    DscFile = open(DscFileName, "w+")
    EdkLogger.info("Save file to %s" % DscFileName)

    StoreHeader(DscFile, Platform.Header)
    StorePlatformDefinesSection(DscFile, Platform)
    StorePlatformBuildOptionsSection(DscFile,Platform)
    StorePlatformSkuIdsSection(DscFile,Platform)
    StorePlatformLibrariesSection(DscFile,Platform) # new in dsc, Edk I components, list of INF files
    StorePlatformLibraryClassesSection(DscFile, Platform) # LibraryClasses are from Modules
    StorePlatformPcdSection(DscFile, Platform)
    #StorePlatformPcdDynamicSection(DscFile, Platform)
    StorePlatformComponentsSection(DscFile,Platform)
    StorePlatformUserExtensionsSection(DscFile,Platform)
    DscFile.close()
    
if __name__ == '__main__':
    pass
