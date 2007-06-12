#!/usr/bin/env python
import sys, os
import EdkLogger

from EdkIIWorkspaceBuild import *
from GenMake import *
from DataType import *
from AutoGenRoutines import *
from PcdDatabaseAutoGen import *
from GenC import *

#
# generate AutoGen.c, AutoGen.h
# parse unicode file and generate XXXXString.h, XXXXString.c
# generate makefile
#

class AutoGen(object):

    PcdTokenNumber = {}     # (TokenSpaceGuidCName, TokenCName) : GeneratedTokenNumber
    DynamicPcdList = []     # [(TokenSpaceGuidCName1, TokenCName1), (TokenSpaceGuidCName2, TokenCName2), ...]
    _TokenNumber = 1

    ModuleDatabase = None
    PackageDatabase = None

    def __init__(self, module, platform, workspace, arch):
        self.Module = module
        self.Platform = platform
        self.Workspace = workspace
        self.Arch = arch

        self.AutoGenC = AutoGenString()
        self.AutoGenH = AutoGenString()
        
        if self.ModuleDatabase == None:
            self.ModuleDatabase = self.Workspace.Build[self.Arch].ModuleDatabase
        if self.PackageDatabase == None:
            self.PackageDatabase = self.Workspace.Build[self.Arch].PackageDatabase

        self.Package = FindModuleOwner(self.Module.DescFilePath, self.PackageDatabase)
        self.GeneratePcdTokenNumber()
        
        if self.Module.LibraryClass != None and self.Module.LibraryClass != "":
            self.IsLibrary = True
            self.LibraryList = []
        else:
            self.IsLibrary = False
            self.LibraryList = self.GetSortedLibraryList()

    def GetSortedLibraryList(self):
        moduleType = self.Module.ModuleType
        libraryConsumerList = [self.Module]
        
        libraryList         = []
        constructor         = []
        consumedByList      = {}

        while len(libraryConsumerList) > 0:
            module = libraryConsumerList.pop()
            for libc, libf in module.LibraryClasses.iteritems():
                if moduleType not in libc or libf == None or libf == "":
                    continue
                
                libm = self.ModuleDatabase[libf]
                if libm not in libraryList:
                    libraryConsumerList.append(libm)
                    libraryList.append(libm)

                if libm.ConstructorList != [] and libm.ConstructorList[0] != [] and libm not in constructor:
                    constructor.append(libm)
                    
                if libm not in consumedByList:
                    consumedByList[libm] = []
                if module != self.Module:
                    if module in consumedByList[libm]:
                        continue
                    consumedByList[libm].append(module)
        #
        # Initialize the sorted output list to the empty set
        #
        SortedLibraryList = []
        #
        # Q <- Set of all nodes with no incoming edges
        #
        Q = []
        for m in libraryList:
            if consumedByList[m] == []:
                Q.insert(0, m)
        #
        # while Q is not empty do
        #
        while Q != []:
            #
            # remove node n from Q
            #
            n = Q.pop()
            #
            # output n
            #
            SortedLibraryList.append(n)
            #
            # for each node m with an edge e from n to m do
            #
            for m in libraryList:
                if n not in consumedByList[m]:
                    continue
                #
                # remove edge e from the graph
                #
                consumedByList[m].remove(n)
                #
                # If m has no other incoming edges then
                #
                if consumedByList[m] == []:
                    #
                    # insert m into Q
                    #
                    Q.insert(0,m)

            EdgeRemoved = True
            while Q == [] and EdgeRemoved:
                EdgeRemoved = False
                #
                # for each node m with a constructor
                #
                for m in libraryList:
                    if m in constructor:
                        #
                        # for each node n without a constructor with an edge e from m to n
                        #
                        for n in consumedByList[m]:
                            if n not in constructor:
                                #
                                # remove edge e from the graph
                                #
                                consumedByList[m].remove(n)
                                EdgeRemoved = True
                                if consumedByList[m] == []:
                                    #
                                    # insert m into Q
                                    #
                                    Q.insert(0,m)
                                    break
                    if Q != []:
                        break

        #
        # if any remaining node m in the graph has a constructor and an incoming edge, then the graph has a cycle
        #
        for m in libraryList:
            if consumedByList[m] != [] and m in constructor:
                EdkLogger.error('Module libraries with constructors have a cycle')

        #
        # Build the list of constructor and destructir names
        # The DAG Topo sort produces the destructor order, so the list of constructors must generated in the reverse order
        #

        SortedLibraryList.reverse()
        return SortedLibraryList

    def GeneratePcdTokenNumber(self):
        if self.PcdTokenNumber != {}:
            return
            
        platformPcds = self.Platform.Pcds
        for key in platformPcds:
            pcd = platformPcds[key]
            if pcd.Type == TAB_PCDS_DYNAMIC and key not in self.PcdTokenNumber:
                self.PcdTokenNumber[key] = self._TokenNumber
                # EdkLogger.info("(%s, %s) = %d (%s)" % (key, self._TokenNumber, pcd.Type))
                self._TokenNumber += 1
                self.DynamicPcdList.append(key)

        for key in platformPcds:
            pcd = platformPcds[key]
            if key not in self.PcdTokenNumber:
                self.PcdTokenNumber[key] = self._TokenNumber
                # EdkLogger.info("(%s, %s) = %d (%s)" % (key, self._TokenNumber, pcd.Type))
                self._TokenNumber += 1

    def PreprocessPcd(self, pcd):
        if pcd.DatumType == None or pcd.DatumType == "" or\
           pcd.TokenValue == None or pcd.TokenValue == "":
            for pkg in self.PackageDatabase:
                package = self.PackageDatabase[pkg]
                key = (pcd.TokenSpaceGuidCName, pcd.TokenCName)
                if key in package.Pcds:
                    pcd.DatumType = package.Pcds[key].DatumType
                    pcd.TokenValue = package.Pcds[key].TokenValue
                    break
        
    def GetPcdList(self):
        platformPcds = self.Platform.Pcds
        EdkLogger.info(self.Module.BaseName + " PCD settings")

        pcdList = []
        for m in self.LibraryList + [self.Module]:
            # EdkLogger.info("  " + m.BaseName)
            modulePcds = m.Pcds
            for key in modulePcds:
                if key not in platformPcds:
                    EdkLogger.error("No matching PCD in platform: %s %s" % key)
                    continue
                pcd = platformPcds[key]
                self.PreprocessPcd(pcd)
                EdkLogger.info("    %s %s %s (%s)" % (pcd.TokenSpaceGuidCName, pcd.TokenCName, pcd.Type, pcd.DatumType))
                pcdList.append(pcd)
        return pcdList

    def CreateModulePcdCode(self, pcd):
        #
        # Write PCDs
        #
        #for TokenSpaceGuidCName in self.Module.Pcds: # Platform.PcdDatabase[ModuleSA]:
        #    for C_Name in Platform.PcdDatabase[ModuleSA][TokenSpaceGuidCName]:
        #      Pcd = Platform.PcdDatabase[ModuleSA][TokenSpaceGuidCName][C_Name]
        pcdTokenName = '_PCD_TOKEN_' + pcd.TokenCName
        if pcd.Type == TAB_PCDS_DYNAMIC_EX:
            tokenNumber = pcd.TokenValue
        else:
            tokenNumber = self.PcdTokenNumber[pcd.TokenSpaceGuidCName, pcd.TokenCName]
        self.AutoGenH.Append('#define %s  %d\n' % (pcdTokenName, tokenNumber))

        datumSize = self.DatumSizeStringDatabase[pcd.DatumType]
        datumSizeLib = self.DatumSizeStringDatabaseLib[pcd.DatumType]
        getModeName = '_PCD_GET_MODE_' + self.DatumSizeStringDatabaseH[pcd.DatumType] + '_' + pcd.TokenCName
        setModeName = '_PCD_SET_MODE_' + self.DatumSizeStringDatabaseH[pcd.DatumType] + '_' + pcd.TokenCName

        if pcd.Type == TAB_PCDS_DYNAMIC_EX:
            self.AutoGenH.Append('#define %s  LibPcdGetEx%s(&%s, %s)\n' % (getModeName, datumSizeLib, pcd.TokenSpaceGuidCName, pcdTokenName))
            if DatumType == 'VOID*':
                self.AutoGenH.Append('#define %s(SizeOfBuffer, Buffer)  LibPcdSetEx%s(&%s, %s, (SizeOfBuffer), (Buffer))\n' % (setModeName, datumSizeLib, pcd.TokenSpaceGuidCName, pcdTokenName))
            else:
                self.AutoGenH.Append('#define %s(Value)  LibPcdSetEx%s(&%s, %s, (Value))\n' % (setModeName, datumSizeLib, pcd.TokenSpaceGuidCName, pcdTokenName))
        elif pcd.Type == TAB_PCDS_DYNAMIC:
            self.AutoGenH.Append('#define %s  LibPcdGet%s(%s)\n' % (getModeName, datumSizeLib, pcdTokenName))
            if pcd.DatumType == 'VOID*':
                self.AutoGenH.Append('#define %s(SizeOfBuffer, Buffer)  LibPcdSet%s(%s, (SizeOfBuffer), (Buffer))\n' %(setModeName, datumSizeLib, pcdTokenName))
            else:
                self.AutoGenH.Append('#define %s(Value)  LibPcdSet%s(%s, (Value))\n' % (setModeName, datumSizeLib, pcdTokenName))
        else:
            PcdVariableName = '_gPcd_' + self.ItemTypeStringDatabase[pcd.Type] + '_' + pcd.TokenCName
            Const = 'const'
            if pcd.Type == TAB_PCDS_PATCHABLE_IN_MODULE:
                Const = ''
            Type = ''
            Array = ''
            Value = pcd.Value
            if pcd.DatumType == 'UINT64':
                Value += 'ULL'
            if pcd.DatumType == 'VOID*':
                ArraySize = int(pcd.MaxDatumSize)
                if Value[0] == '{':
                    Type = '(VOID *)'
                else:
                    Unicode = False
                    if Value[0] == 'L':
                        Unicode = True
                    Value = Value.lstrip('L').strip('"')
                    NewValue = '{'
                    for Index in range(0,len(Value)):
                        NewValue = NewValue + str(ord(Value[Index]) % 0x100) + ', '
                        if Unicode:
                            NewValue = NewValue + str(ord(Value[Index]) / 0x100) + ', '
                    if Unicode:
                        if ArraySize < (len(Value)*2 + 2):
                            ArraySize = len(Value)*2 + 2
                        NewValue = NewValue + '0, '
                    else:
                        if ArraySize < (len(Value) + 1):
                            ArraySize = len(Value) + 1
                    Value = NewValue + '0 }'
                Array = '[%d]' % ArraySize

            PcdValueName = '_PCD_VALUE_' + pcd.TokenCName
            if pcd.DatumType == 'VOID*' and Value[0] == '{':
                self.AutoGenH.Append('#define _PCD_PATCHABLE_%s_SIZE %s\n' % (pcd.TokenCName, pcd.MaxDatumSize))
                self.AutoGenH.Append('#define %s  %s%s\n' %(PcdValueName, Type, PcdVariableName))
                self.AutoGenC.Append('GLOBAL_REMOVE_IF_UNREFERENCED %s UINT8 %s%s = %s;\n' % (Const, PcdVariableName, Array, Value))
                self.AutoGenH.Append('extern %s UINT8 %s%s;\n' %(Const, PcdVariableName, Array))
                self.AutoGenH.Append('#define %s  %s%s\n' %(getModeName, Type, PcdVariableName))
            else:
                self.AutoGenH.Append('#define %s  %s\n' %(PcdValueName, Value))
                self.AutoGenC.Append('GLOBAL_REMOVE_IF_UNREFERENCED %s %s %s = %s;\n' %(Const, pcd.DatumType, PcdVariableName, PcdValueName))
                self.AutoGenH.Append('extern %s  %s  %s%s;\n' % (Const, pcd.DatumType, PcdVariableName, Array))
                self.AutoGenH.Append('#define %s  %s%s\n' % (getModeName, Type, PcdVariableName))

            if pcd.Type == 'PATCHABLE_IN_MODULE':
                if pcd.DatumType == 'VOID*':
                    self.AutoGenH.Append('#define %s(SizeOfBuffer, Buffer)  LibPatchPcdSetPtr(_gPcd_BinaryPatch_%s, (UINTN)_PCD_PATCHABLE_%s_SIZE, (SizeOfBuffer), (Buffer))\n' % (setModeName, pcd.TokenCName, pcd.TokenCName))
                else:
                    self.AutoGenH.Append('#define %s(Value)  (%s = (Value))\n' % (setModeName, PcdVariableName))
            else:
                self.AutoGenH.Append('//#define %s  ASSERT(FALSE)  // It is not allowed to set value for a FIXED_AT_BUILD PCD\n' % setModeName)

    def CreateLibraryPcdCode(self, pcd):
        tokenSpaceGuidCName = pcd.TokenSpaceGuidCName
        tokenCName  = pcd.TokenCName
        tokenNumber = self.PcdTokenNumber[tokenSpaceGuidCName, tokenCName]
        datumType   = pcd.DatumType
        datumSize   = DatumSizeStringDatabaseH[datumType]
        datumSizeLib= DatumSizeStringDatabaseLib[datumType]
        getModeName = '_PCD_GET_MODE_' + datumSize + '_' + tokenCName
        setModeName = '_PCD_SET_MODE_' + datumSize + '_' + tokenCName
        
        type = ''
        array = ''
        if pcd.DatumType == 'VOID*':
            type = '(VOID *)'
            array = '[]'

        self.AutoGenH.Append('#define _PCD_TOKEN_%s  %d\n' % (tokenCName, tokenNumber))

        pcdItemType = pcd.Type
        if pcdItemType == TAB_PCDS_DYNAMIC:
            pcdItemType = TAB_PCDS_FIXED_AT_BUILD
            for SearchModuleSA in Platform.PcdDatabase:
                if TokenSpaceGuidCName not in Platform.PcdDatabase[SearchModuleSA]:
                    continue
                if tokenCName not in Platform.PcdDatabase[SearchModuleSA][TokenSpaceGuidCName]:
                    continue
                pcdItemType  = Platform.PcdDatabase[SearchModuleSA][TokenSpaceGuidCName][tokenCName].Type
                break
        if pcdItemType == TAB_PCDS_DYNAMIC_EX:
            pcdTokenName = '_PCD_TOKEN_' + tokenCName
            self.AutoGenH.Append('#define %s  LibPcdGetEx%s(&%s, %s)\n' % (getModeName, datumSizeLib, tokenSpaceGuidCName, pcdTokenName))
            if DatumType == 'VOID*':
                self.AutoGenH.Append('#define %s(SizeOfBuffer, Buffer)  LibPcdSetEx%s(&%s, %s, (SizeOfBuffer), (Buffer))\n' % (setModeName,datumSizeLib, tokenSpaceGuidCName, pcdTokenName))
            else:
                self.AutoGenH.Append('#define %s(Value)  LibPcdSetEx%s(&%s, %s, (Value))\n' % (setModeName, datumSizeLib, tokenSpaceGuidCName, pcdTokenName))
        if pcdItemType == TAB_PCDS_DYNAMIC:
            pcdTokenName = '_PCD_TOKEN_' + tokenCName
            self.AutoGenH.Append('#define %s  LibPcdGet%s(%s)\n' % (getModeName, datumSizeLib, pcdTokenName))
            if datumType == 'VOID*':
                self.AutoGenH.Append('#define %s(SizeOfBuffer, Buffer)  LibPcdSet%s(%s, (SizeOfBuffer), (Buffer))\n' %(setModeName, datumSizeLib, pcdTokenName))
            else:
                self.AutoGenH.Append('#define %s(Value)  LibPcdSet%s(%s, (Value))\n' % (setModeName, datumSizeLib, pcdTokenName))
        if pcdItemType == TAB_PCDS_PATCHABLE_IN_MODULE:
            pcdVariableName = '_gPcd_' + ItemTypeStringDatabase[TAB_PCDS_PATCHABLE_IN_MODULE] + '_' + tokenCName
            self.AutoGenH.Append('extern %s _gPcd_BinaryPatch_%s%s;\n' %(datumType, tokenCName, array) )
            self.AutoGenH.Append('#define %s  %s_gPcd_BinaryPatch_%s\n' %(getModeName, type, tokenCName))
            self.AutoGenH.Append('#define %s(Value)  (%s = (Value))\n' % (setModeName, pcdVariableName))
        if pcdItemType == TAB_PCDS_FIXED_AT_BUILD or pcdItemType == TAB_PCDS_FEATURE_FLAG:
            self.AutoGenH.Append('extern const %s _gPcd_FixedAtBuild_%s%s;\n' %(datumType, tokenCName, array))
            self.AutoGenH.Append('#define %s  %s_gPcd_FixedAtBuild_%s\n' %(getModeName, type, tokenCName))
            self.AutoGenH.Append('//#define %s  ASSERT(FALSE)  // It is not allowed to set value for a FIXED_AT_BUILD PCD\n' % setModeName)

    def GetGuidValue(self, guidCName):
        for Package in self.PackageDatabase.values():
            if guidCName in Package.Guids:
                return Package.Guids[guidCName]
        return None

    def CreatePcdDatabasePhaseSpecificAutoGen (Platform, Phase):
      AutoGenC = AutoGenString()
      AutoGenH = AutoGenString()

      Dict = {
        'PHASE'                         : Phase,
        'GUID_TABLE_SIZE'               : '1',
        'STRING_TABLE_SIZE'             : '1',
        'SKUID_TABLE_SIZE'              : '1',
        'LOCAL_TOKEN_NUMBER_TABLE_SIZE' : '1',
        'LOCAL_TOKEN_NUMBER'            : '0',
        'EXMAPPING_TABLE_SIZE'          : '1',
        'EX_TOKEN_NUMBER'               : '0',
        'SIZE_TABLE_SIZE'               : '2',
        'GUID_TABLE_EMPTY'              : 'TRUE',
        'STRING_TABLE_EMPTY'            : 'TRUE',
        'SKUID_TABLE_EMPTY'             : 'TRUE',
        'DATABASE_EMPTY'                : 'TRUE',
        'EXMAP_TABLE_EMPTY'             : 'TRUE',
        'PCD_DATABASE_UNINIT_EMPTY'     : '  UINT8  dummy; /* PCD_DATABASE_UNINIT is emptry */',
        'SYSTEM_SKU_ID'                 : '  SKU_ID             SystemSkuId;',
        'SYSTEM_SKU_ID_VALUE'           : '0'
      }

      for DatumType in ['UINT64','UINT32','UINT16','UINT8','BOOLEAN']:
        Dict['VARDEF_CNAME_'+DatumType] = []
        Dict['VARDEF_GUID_'+DatumType]  = []
        Dict['VARDEF_SKUID_'+DatumType] = []
        Dict['VARDEF_VALUE_'+DatumType] = []
        for Init in ['INIT','UNINIT']:
          Dict[Init+'_CNAME_DECL_'+DatumType]   = []
          Dict[Init+'_GUID_DECL_'+DatumType]    = []
          Dict[Init+'_NUMSKUS_DECL_'+DatumType] = []
          Dict[Init+'_VALUE_'+DatumType]        = []

      for Type in ['STRING_HEAD','VPD_HEAD','VARIABLE_HEAD']:
        Dict[Type+'_CNAME_DECL']   = []
        Dict[Type+'_GUID_DECL']    = []
        Dict[Type+'_NUMSKUS_DECL'] = []
        Dict[Type+'_VALUE'] = []

      Dict['STRING_TABLE_INDEX'] = []
      Dict['STRING_TABLE_LENGTH']  = []
      Dict['STRING_TABLE_CNAME'] = []
      Dict['STRING_TABLE_GUID']  = []
      Dict['STRING_TABLE_VALUE'] = []

      Dict['SIZE_TABLE_CNAME'] = []
      Dict['SIZE_TABLE_GUID']  = []
      Dict['SIZE_TABLE_CURRENT_LENGTH']  = []
      Dict['SIZE_TABLE_MAXIMUM_LENGTH']  = []

      Dict['EXMAPPING_TABLE_EXTOKEN'] = []
      Dict['EXMAPPING_TABLE_LOCAL_TOKEN'] = []
      Dict['EXMAPPING_TABLE_GUID_INDEX'] = []

      Dict['GUID_STRUCTURE'] = []

      Dict['SKUID_VALUE'] = []

      if Phase == 'DXE':
        Dict['SYSTEM_SKU_ID'] = ''
        Dict['SYSTEM_SKU_ID_VALUE'] = ''

      StringTableIndex = 0
      StringTableSize = 0
      NumberOfLocalTokens = 0
      NumberOfPeiLocalTokens = 0
      NumberOfDxeLocalTokens = 0
      NumberOfExTokens = 0
      NumberOfSizeItems = 0
      GuidList = []

      platformPcds = self.Platform.Pcds
      for TokenSpaceGuidCName, CName in self.DynamicPcdList:
          Pcd = platformPcds[TokenSpaceGuidCName, CName]
          if Pcd.Phase == 'PEI':
            NumberOfPeiLocalTokens += 1
          if Pcd.Phase == 'DXE':
            NumberOfDxeLocalTokens += 1
          if Pcd.Phase != Phase:
            continue


          TokenSpaceGuid = self.GetGuidValue(TokenSpaceGuidCName)
          if Pcd.Type == 'DYNAMIC_EX':
            if TokenSpaceGuid not in GuidList:
              GuidList += [TokenSpaceGuid]
              Dict['GUID_STRUCTURE'].append(TokenSpaceGuid)
            NumberOfExTokens += 1

          ValueList = []
          StringHeadOffsetList = []
          VpdHeadOffsetList = []
          VariableHeadValueList = []
          Pcd.InitString = 'UNINIT'
          if Pcd.DatumType == 'VOID*':
            Pcd.TokenTypeList = ['PCD_DATUM_TYPE_POINTER']
          elif Pcd.DatumType == 'BOOLEAN':
            Pcd.TokenTypeList = ['PCD_DATUM_TYPE_UINT8']
          else:
            Pcd.TokenTypeList = ['PCD_DATUM_TYPE_'+Pcd.DatumType]
          if len(Pcd.SkuInfo) > 1:
            Pcd.TokenTypeList += ['PCD_TYPE_SKU_ENABLED']

          for SkuId in Pcd.SkuInfo:
            if SkuId == '':
              continue
            if SkuId not in Dict['SKUID_VALUE']:
              Dict['SKUID_VALUE'].append(SkuId)

            SkuIdIndex =   Dict['SKUID_VALUE'].index(SkuId)
            Sku = Pcd.SkuInfo[SkuId]
            if len(Sku.VariableName) > 0:
              Pcd.TokenTypeList += ['PCD_TYPE_HII']
              Pcd.InitString = 'INIT'
              VariableNameStructure = '{' + ', '.join(Sku.VariableName) + ', 0x0000}'
              if VariableNameStructure not in Dict['STRING_TABLE_VALUE']:
                Dict['STRING_TABLE_CNAME'].append(CName)
                Dict['STRING_TABLE_GUID'].append(TokenSpaceGuid.replace('-','_'))
                if StringTableIndex == 0:
                  Dict['STRING_TABLE_INDEX'].append('')
                else:
                  Dict['STRING_TABLE_INDEX'].append('_%d' % StringTableIndex)

                Dict['STRING_TABLE_LENGTH'].append(len(Sku.VariableName) + 1)
                Dict['STRING_TABLE_VALUE'].append(VariableNameStructure)
                StringTableIndex += 1
                StringTableSize += len(Sku.VariableName) + 1

              VariableHeadStringIndex = 0
              for Index in range(Dict['STRING_TABLE_VALUE'].index(VariableNameStructure)):
                VariableHeadStringIndex += Dict['STRING_TABLE_LENGTH'][Index]

              VariableGuid = self.GetGuidValue(Sku.VariableGuid)
              if VariableGuid not in GuidList:
                GuidList += [VariableGuid]
                Dict['GUID_STRUCTURE'].append(VariableGuid)
              VariableHeadGuidIndex = GuidList.index(VariableGuid)

              VariableHeadValueList.append('%d, %d, %s, offsetof(${PHASE}_PCD_DATABASE, Init.%s_%s_VariableDefault_%s)' %
                (VariableHeadGuidIndex, VariableHeadStringIndex, Sku.VariableOffset, CName, TokenSpaceGuid.replace('-','_'), SkuIdIndex))
              Dict['VARDEF_CNAME_'+Pcd.DatumType].append(CName)
              Dict['VARDEF_GUID_'+Pcd.DatumType].append(TokenSpaceGuid.replace('-','_'))
              Dict['VARDEF_SKUID_'+Pcd.DatumType].append(SkuIdIndex)
              Dict['VARDEF_VALUE_'+Pcd.DatumType].append(Sku.HiiDefaultValue)
            elif Sku.VpdOffset != '':
              Pcd.TokenTypeList += ['PCD_TYPE_VPD']
              Pcd.InitString = 'INIT'
              VpdHeadOffsetList.append(Sku.VpdOffset)
            else:
              if Pcd.DatumType == 'VOID*':
                Pcd.TokenTypeList += ['PCD_TYPE_STRING']
                Pcd.InitString = 'INIT'
                if Sku.Value != '':
                  NumberOfSizeItems += 1
                  Dict['STRING_TABLE_CNAME'].append(CName)
                  Dict['STRING_TABLE_GUID'].append(TokenSpaceGuid.replace('-','_'))
                  if StringTableIndex == 0:
                    Dict['STRING_TABLE_INDEX'].append('')
                  else:
                    Dict['STRING_TABLE_INDEX'].append('_%d' % StringTableIndex)
                  if Sku.Value[0] == 'L':
                    Size = len(Sku.Value) - 3
                    Dict['STRING_TABLE_VALUE'].append(Sku.Value)
                  elif Sku.Value[0] == '"':
                    Size = len(Sku.Value) - 2
                    Dict['STRING_TABLE_VALUE'].append(Sku.Value)
                  elif Sku.Value[0] == '{':
                    Size = len(Sku.Value.replace(',',' ').split())
                    Dict['STRING_TABLE_VALUE'].append('{' + Sku.Value + '}')
                  StringHeadOffsetList.append(str(StringTableSize))
                  Dict['SIZE_TABLE_CNAME'].append(CName)
                  Dict['SIZE_TABLE_GUID'].append(TokenSpaceGuid.replace('-','_'))
                  Dict['SIZE_TABLE_CURRENT_LENGTH'].append(Size)
                  Dict['SIZE_TABLE_MAXIMUM_LENGTH'].append(Pcd.MaxDatumSize)
                  if Pcd.MaxDatumSize != '' and Pcd.MaxDatumSize > Size:
                    Size = int(Pcd.MaxDatumSize)
                  Dict['STRING_TABLE_LENGTH'].append(Size)
                  StringTableIndex += 1
                  StringTableSize += Size
              else:
                Pcd.TokenTypeList += ['PCD_TYPE_DATA']
                if Sku.Value == 'TRUE':
                  Pcd.InitString = 'INIT'
                elif Sku.Value.find('0x') == 0:
                  if int(Sku.Value,16) != 0:
                    Pcd.InitString = 'INIT'
                elif Sku.Value[0].isdigit():
                  if int(Sku.Value) != 0:
                    Pcd.InitString = 'INIT'
                ValueList.append(Sku.Value)
          Pcd.TokenTypeList =list(set(Pcd.TokenTypeList))
          if 'PCD_TYPE_HII' in Pcd.TokenTypeList:
            Dict['VARIABLE_HEAD_CNAME_DECL'].append(CName)
            Dict['VARIABLE_HEAD_GUID_DECL'].append(TokenSpaceGuid.replace('-','_'))
            Dict['VARIABLE_HEAD_NUMSKUS_DECL'].append(len(Pcd.SkuInfo))
            Dict['VARIABLE_HEAD_VALUE'].append('{ %s }\n' % ' },\n    { '.join(VariableHeadValueList))
          if 'PCD_TYPE_VPD' in Pcd.TokenTypeList:
            Dict['VPD_HEAD_CNAME_DECL'].append(CName)
            Dict['VPD_HEAD_GUID_DECL'].append(TokenSpaceGuid.replace('-','_'))
            Dict['VPD_HEAD_NUMSKUS_DECL'].append(len(Pcd.SkuInfo))
            Dict['VPD_HEAD_VALUE'].append('{ %s }' % ' }, { '.join(VpdHeadOffsetList))
          if 'PCD_TYPE_STRING' in Pcd.TokenTypeList:
            Dict['STRING_HEAD_CNAME_DECL'].append(CName)
            Dict['STRING_HEAD_GUID_DECL'].append(TokenSpaceGuid.replace('-','_'))
            Dict['STRING_HEAD_NUMSKUS_DECL'].append(len(Pcd.SkuInfo))
            Dict['STRING_HEAD_VALUE'].append(', '.join(StringHeadOffsetList))
          if 'PCD_TYPE_DATA' in Pcd.TokenTypeList:
            Dict[Pcd.InitString+'_CNAME_DECL_'+Pcd.DatumType].append(CName)
            Dict[Pcd.InitString+'_GUID_DECL_'+Pcd.DatumType].append(TokenSpaceGuid.replace('-','_'))
            Dict[Pcd.InitString+'_NUMSKUS_DECL_'+Pcd.DatumType].append(len(Pcd.SkuInfo))
            if Pcd.InitString == 'UNINIT':
              Dict['PCD_DATABASE_UNINIT_EMPTY'] = ''
            else:
              Dict[Pcd.InitString+'_VALUE_'+Pcd.DatumType].append(', '.join(ValueList))

      if Phase == 'PEI':
        NumberOfLocalTokens = NumberOfPeiLocalTokens
      if Phase == 'DXE':
        NumberOfLocalTokens = NumberOfDxeLocalTokens

      Dict['TOKEN_INIT']       = ['' for x in range(NumberOfLocalTokens)]
      Dict['TOKEN_CNAME']      = ['' for x in range(NumberOfLocalTokens)]
      Dict['TOKEN_GUID']       = ['' for x in range(NumberOfLocalTokens)]
      Dict['TOKEN_TYPE']       = ['' for x in range(NumberOfLocalTokens)]

      for TokenSpaceGuidCName in Platform.DynamicPcdBuildDefinitions:
        for CName in Platform.DynamicPcdBuildDefinitions[TokenSpaceGuidCName]:
          Pcd = Platform.DynamicPcdBuildDefinitions[TokenSpaceGuidCName][CName]
          if Pcd.Phase != Phase:
            continue
          for Package in Platform.PackageList:
            if TokenSpaceGuidCName in Package.GuidDatabase:
              TokenSpaceGuid = Package.GuidDatabase[TokenSpaceGuidCName].Guid.lower()
              break
          GeneratedTokenNumber = Pcd.GeneratedTokenNumber - 1
          if Phase == 'DXE':
            GeneratedTokenNumber -= NumberOfPeiLocalTokens
          Dict['TOKEN_INIT'][GeneratedTokenNumber] = 'Init'
          if Pcd.InitString == 'UNINIT':
            Dict['TOKEN_INIT'][GeneratedTokenNumber] = 'Uninit'
          Dict['TOKEN_CNAME'][GeneratedTokenNumber] = CName
          Dict['TOKEN_GUID'][GeneratedTokenNumber] = TokenSpaceGuid.replace('-','_')
          Dict['TOKEN_TYPE'][GeneratedTokenNumber] = ' | '.join(Pcd.TokenTypeList)
          if Pcd.ItemType == 'DYNAMIC_EX':
            Dict['EXMAPPING_TABLE_EXTOKEN'].append(Pcd.Token)
            Dict['EXMAPPING_TABLE_LOCAL_TOKEN'].append(GeneratedTokenNumber)
            Dict['EXMAPPING_TABLE_GUID_INDEX'].append(GuidList.index(TokenSpaceGuid))

      if GuidList != []:
        Dict['GUID_TABLE_EMPTY'] = 'FALSE'
        Dict['GUID_TABLE_SIZE'] = len(GuidList)
      else:
        Dict['GUID_STRUCTURE'] = [GuidStringToGuidStructureString('00000000-0000-0000-0000-000000000000')]
      if StringTableIndex == 0:
        Dict['STRING_TABLE_INDEX'].append('')
        Dict['STRING_TABLE_LENGTH'].append(1)
        Dict['STRING_TABLE_CNAME'].append('')
        Dict['STRING_TABLE_GUID'].append('')
        Dict['STRING_TABLE_VALUE'].append('{ 0 }')
      else:
        Dict['STRING_TABLE_EMPTY'] = 'FALSE'
        Dict['STRING_TABLE_SIZE'] = StringTableSize
      if Dict['SIZE_TABLE_CNAME'] == []:
        Dict['SIZE_TABLE_CNAME'].append('')
        Dict['SIZE_TABLE_GUID'].append('')
        Dict['SIZE_TABLE_CURRENT_LENGTH'].append(0)
        Dict['SIZE_TABLE_MAXIMUM_LENGTH'].append(0)
      if NumberOfLocalTokens != 0:
        Dict['DATABASE_EMPTY']                = 'FALSE'
        Dict['LOCAL_TOKEN_NUMBER_TABLE_SIZE'] = NumberOfLocalTokens
        Dict['LOCAL_TOKEN_NUMBER']            = NumberOfLocalTokens
      if NumberOfExTokens != 0:
        Dict['EXMAP_TABLE_EMPTY']    = 'FALSE'
        Dict['EXMAPPING_TABLE_SIZE'] = NumberOfExTokens
        Dict['EX_TOKEN_NUMBER']      = NumberOfExTokens
      else:
        Dict['EXMAPPING_TABLE_EXTOKEN'].append(0)
        Dict['EXMAPPING_TABLE_LOCAL_TOKEN'].append(0)
        Dict['EXMAPPING_TABLE_GUID_INDEX'].append(0)

      if NumberOfSizeItems != 0:
        Dict['SIZE_TABLE_SIZE'] = NumberOfSizeItems * 2
      AutoGenH.Append(PcdDatabaseAutoGenH, Dict)

      if NumberOfLocalTokens == 0:
        AutoGenC.Append(EmptyPcdDatabaseAutoGenC, Dict)
      else:
        AutoGenC.Append(PcdDatabaseAutoGenC, Dict)

      return AutoGenH, AutoGenC

    def CreatePcdDatabaseCode (Platform, Phase):
        AutoGenC = AutoGenString()
        AutoGenH = AutoGenString()
        AutoGenH.Append(PcdDatabaseCommonAutoGenH)
        AdditionalAutoGenH, AdditionalAutoGenC = CreatePcdDatabasePhaseSpecificAutoGen (Platform, 'PEI')
        AutoGenH.Append(AdditionalAutoGenH.String)
        if Phase == 'PEI':
            AutoGenC.Append(AdditionalAutoGenC.String)
        if Phase == 'DXE':
            AdditionalAutoGenH, AdditionalAutoGenC = CreatePcdDatabasePhaseSpecificAutoGen (Platform, Phase)
            AutoGenH.Append(AdditionalAutoGenH.String)
            AutoGenC.Append(AdditionalAutoGenC.String)
            AutoGenH.Append(PcdDatabaseEpilogueAutoGenH)
        return AutoGenH, AutoGenC

    def CreateLibraryConstructorCode(self):
        #
        # Library Constructors
        #
        ConstructorList = []
        for lib in self.LibraryList:
            if len(lib.ConstructorList) <= 0:
                continue
            ConstructorList.extend(lib.ConstructorList)
            
        Dict = {'Type':'Constructor', 'Function':ConstructorList}
        if self.Module.ModuleType == 'BASE':
            if len(ConstructorList) == 0:
                AutoGenC.Append(LibraryString[0], Dict)
            else:
                AutoGenC.Append(LibraryString[3], Dict)
        elif self.Module.ModuleType in ['PEI_CORE','PEIM']:
            if len(ConstructorList) == 0:
                AutoGenC.Append(LibraryString[1], Dict)
            else:
                AutoGenC.Append(LibraryString[4], Dict)
        elif self.Module.ModuleType in ['DXE_CORE','DXE_DRIVER','DXE_SMM_DRIVER','DXE_RUNTIME_DRIVER','DXE_SAL_DRIVER','UEFI_DRIVER','UEFI_APPLICATION']:
            if len(ConstructorList) == 0:
                AutoGenC.Append(LibraryString[2], Dict)
            else:
                AutoGenC.Append(LibraryString[5], Dict)

    def CreateLibraryDestructorCode(self):
        #
        # Library Destructors
        #
        DestructorList = []
        for lib in self.LibraryList:
            if len(lib.DestructorList) <= 0:
                continue
            DestructorList.extend(lib.DestructorList)

        DestructorList.reverse()
        if self.Module.ModuleType in ['DXE_CORE','DXE_DRIVER','DXE_SMM_DRIVER','DXE_RUNTIME_DRIVER','DXE_SAL_DRIVER','UEFI_DRIVER','UEFI_APPLICATION']:
            if len(DestructorList) == 0:
                AutoGenC.Append(LibraryString[2], {'Type':'Destructor','Function':DestructorList})
            else:
                AutoGenC.Append(LibraryString[5], {'Type':'Destructor','Function':DestructorList})


    def CreateModuleEntryPointCode(self):
        #
        # Module Entry Points
        #
        NumEntryPoints = len(self.Module.ModuleEntryPointList)
        Dict = {'Function':self.Module.ModuleEntryPointList}
        
        if self.Module.ModuleType in ['PEI_CORE', 'DXE_CORE']:
            if NumEntryPoints != 1:
                EdkLogger.error('ERROR: %s must have exactly one entry point' % self.Module.ModuleType)
        if self.Module.ModuleType == 'PEI_CORE':
            self.AutoGenC.Append(PeiCoreEntryPointString, Dict)
        elif self.Module.ModuleType == 'DXE_CORE':
            self.AutoGenC.Append(DxeCoreEntryPointString, Dict)
        elif self.Module.ModuleType == 'PEIM':
            if NumEntryPoints < 2:
                self.AutoGenC.Append(PeimEntryPointString[NumEntryPoints], Dict)
            else:
                self.AutoGenC.Append(PeimEntryPointString[2], Dict)
        elif self.Module.ModuleType in ['DXE_RUNTIME_DRIVER','DXE_DRIVER','DXE_SMM_DRIVER', 'DXE_SAL_DRIVER','UEFI_DRIVER','UEFI_APPLICATION']:
            if self.Module.ModuleType == 'DXE_SMM_DRIVER':
                if NumEntryPoints == 0:
                    self.AutoGenC.Append(DxeSmmEntryPointString[0], Dict)
                else:
                    self.AutoGenC.Append(DxeSmmEntryPointString[1], Dict)
            else:
                if NumEntryPoints < 2:
                    self.AutoGenC.Append(UefiEntryPointString[NumEntryPoints], Dict)
                else:
                    self.AutoGenC.Append(UefiEntryPointString[2], Dict)

    def CreateModuleUnloadImageCode(self):
        #
        # Unload Image Handlers
        #
        NumUnloadImage = len(self.Module.ModuleUnloadImageList)
        Dict = {'Count':NumUnloadImage, 'Function':self.Module.ModuleUnloadImageList}
        if NumUnloadImage < 2:
            self.AutoGenC.Append(UefiUnloadImageString[NumUnloadImage], Dict)
        else:
            self.AutoGenC.Append(UefiUnloadImageString[2], Dict)

    def CreateGuidDefinitionCode(self):
        #
        # GUIDs
        #
        for Key in self.Module.Guids:
            for pkg in self.Module.Packages:
                Package = self.PackageDatabase[pkg]
                if Key in Package.Guids:
                    self.AutoGenC.Append('GLOBAL_REMOVE_IF_UNREFERENCED EFI_GUID  %s = %s;\n' % (Key, Package.Guids[Key]))
                    break
            else:
                EdkLogger.error('ERROR: GUID %s not found in dependent packages of module %s' % (Key, self.Module.BaseName))

    def CreateProtocolDefinitionCode(self):
        #
        # Protocol GUIDs
        #
        for Key in self.Module.Protocols:
            for pkg in self.Module.Packages:
                Package = self.PackageDatabase[pkg]
                if Key in Package.Protocols:
                    self.AutoGenC.Append('GLOBAL_REMOVE_IF_UNREFERENCED EFI_GUID  %s = %s;\n' % (Key, Package.Protocols[Key]))
                    break
            else:
                EdkLogger.error('ERROR: Protocol %s not found in dependent packages of module %s' % (Key, self.Module.BaseName))

    def CreatePpiDefinitionCode(self):
        #
        # PPI GUIDs
        #
        for Key in self.Module.Ppis:
            for pkg in self.Module.Packages:
                Package = self.PackageDatabase[pkg]
                if Key in Package.Ppis:
                    self.AutoGenC.Append('GLOBAL_REMOVE_IF_UNREFERENCED EFI_GUID  %s = %s;\n' % (Key, Package.Ppis[Key]))
                    break
            else:
                EdkLogger.error('ERROR: PPI %s not found in dependent packages of module %s' % (Key, self.Module.BaseName))

    def CreateSpecificationCode(self):
        self.AutoGenH.Append(SpecificationString,   {'Specification':self.Module.Specification})
        
    def CreatePcdCode(self):
        if self.IsLibrary:
            self.CreateLibraryPcdCode()
        else:
            self.CreateModulePcdCode()

    def CreateHeaderCode(self):
        AutoGenC.Append(AutoGenHeaderString, {'FileName':'AutoGen.c'})
        
        AutoGenH.Append(AutoGenHeaderString,   {'FileName':'AutoGen.h'})
        AutoGenH.Append(AutoGenHPrologueString,{'Guid':self.Module.Guid.replace('-','_')})

        #
        # Publish the CallerId Guid
        #
        if self.Module.ModuleType == 'BASE':
            AutoGenC.Append('\nGLOBAL_REMOVE_IF_UNREFERENCED GUID  gEfiCallerIdGuid = %s;\n' % GuidStringToGuidStructureString(self.Module.Guid))
        else:
            AutoGenC.Append('\nGLOBAL_REMOVE_IF_UNREFERENCED EFI_GUID  gEfiCallerIdGuid = %s;\n' % GuidStringToGuidStructureString(self.Module.Guid))

    def CreateFooterCode(self):
        AutoGenH.Append(AutoGenHEpilogueString)

    def CreateCode(self, filePath):
        self.CreateHeaderCode()
        
        self.CreateModuleEntryPointCode()
        self.CreateModuleUnloadImageCode()
        self.CreateLibraryConstructorCode()
        self.CreateLibraryDestructorCode()
        self.CreateGuidDefinitionCode()
        self.CreateProtocolDefinitionCode()
        self.CreatePpiDefinitionCode()
        self.CreatePcdCode()
        
        self.CreateFooterCode()

        CreateDirectory(filePath)
        autoGenH = open(os.path.join(filePath, "AutoGen.h"), "w")
        autoGenH.write(self.AutoGenH.String)

        if not self.IsLibrary:
            autoGenC = open(os.path.join(filePath, "AutoGen.c"), "w")
            autoGenC.write(self.AutoGenC.String)

# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    print "Running Operating System =", sys.platform
    ewb = WorkspaceBuild()
    #print ewb.Build.keys()

    myArch = ewb.Build["IA32"].Arch
    print myArch

    myBuild = ewb.Build["IA32"]

    myWorkspace = ewb
    apf = ewb.TargetTxt.TargetTxtDictionary["ACTIVE_PLATFORM"][0]
    myPlatform = myBuild.PlatformDatabase[os.path.normpath(apf)]

    #LoadBuildRule(myWorkspace.Workspace.WorkspaceFile('Tools/Conf/build.rule'))

    myToolchain = ewb.TargetTxt.TargetTxtDictionary["TOOL_CHAIN_TAG"][0]
    #print myToolchain

    myBuildTarget = ewb.TargetTxt.TargetTxtDictionary["TARGET"][0]
    #print myBuildTarget

    myBuildOption = {
        "ENABLE_PCH"        :   False,
        "ENABLE_LOCAL_LIB"  :   True,
    }

    for mf in myBuild.ModuleDatabase:
        #mf = "MdePkg\\Library\\BaseLib\\BaseLib.inf"
        #if mf in myPlatform.Modules and mf in myBuild.ModuleDatabase:
        #print mf

        myModule = myBuild.ModuleDatabase[mf]
        if myModule.LibraryClass != None and myModule.LibraryClass != "":
            continue    # skip library instance

        ag = AutoGen(myModule, myPlatform, myWorkspace, myArch)
        print myModule.BaseName,"(%s)" % myModule
        for lm in ag.LibraryList:
            if lm.ConstructorList[0] != []:
                print "  %-40s:%40s" % (lm.BaseName, lm.ConstructorList[0])
            else:
                print "  %s:" % lm.BaseName
                
        ag.CreateCode(os.path.join("tmp", myModule.BaseName))
