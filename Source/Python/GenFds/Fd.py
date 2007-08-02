import Region
import Fv
import os
import StringIO
import sys
from struct import *
from GenFdsGlobalVariable import GenFdsGlobalVariable
T_CHAR_LF = '\n'
from CommonDataClass.FdfClassObject import FDClassObject

class FD(FDClassObject):
    def __init__(self):
        FDClassObject.__init__(self)

    """  Create Fd file """
    
    def GenFd (self, FvBinDict):
        #
        # Print Information
        #
        GenFdsGlobalVariable.InfLogger("Fd File Name:%s" %self.FdUiName)
        GenFdsGlobalVariable.VerboseLogger('Following Fv will be add to Fd !!!')
        for item in GenFdsGlobalVariable.FdfParser.profile.FvDict:
            GenFdsGlobalVariable.VerboseLogger(item)

        GenFdsGlobalVariable.VerboseLogger('################### Gen VTF ####################')
        self.GenVtfFile()
        
        FdBuffer = StringIO.StringIO('')
        for Regions in self.RegionList :
            #
            # Call each region's AddToBuffer function 
            #
            GenFdsGlobalVariable.VerboseLogger('Call each region\'s AddToBuffer function')
            Regions.AddToBuffer (FdBuffer, self.BaseAddress, self.BlockSizeList, self.ErasePolarity, FvBinDict, self.vtfRawDict)
        #
        # Create a empty Fd file
        #
        GenFdsGlobalVariable.VerboseLogger ('Create a empty Fd file')
        FdFileName = os.path.join(GenFdsGlobalVariable.FvDir,
                                  self.FdUiName + '.fd')
        fd = open(FdFileName, 'w+b')
       
        #
        # Write the buffer contents to Fd file
        #
        GenFdsGlobalVariable.VerboseLogger('Write the buffer contents to Fd file')
        fd.write(FdBuffer.getvalue());
        fd.close;
        FdBuffer.close;
        
    def GenVtfFile (self) :
        #
        # Get this Fd's all Fv name
        #
        fvAddDict ={}
        fvList = []
        for region in self.RegionList:
            if region.RegionType == 'FV':
                if len(region.RegionDataList) == 1:
                    RegionData = region.RegionDataList[0]
                    fvList.append(RegionData.upper())
                    fvAddDict[RegionData.upper()] = (int(self.BaseAddress,16) + \
                                                region.Offset, region.Size)
                else:
                    Offset = region.Offset
                    for RegionData in region.RegionDataList:
                        fvList.append(RegionData.upper())
                        fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(RegionData.upper())
                        if len(fv.BlockSizeList) < 1:
                            raise Exception ('FV.%s must point out FVs blocksize and Fv BlockNum' %fv.UiFvName)
                        else:
                            Size = 0
                            for blockStatement in fv.BlockSizeList:
                                Size = Size + blockStatement[0] * blockStatement[1]
                            fvAddDict[RegionData.upper()] = (int(self.BaseAddress,16) + \
                                                             Offset, Size)
                            Offset = Offset + Size
        #
        # Check whether this Fd need VTF
        #
        flag = False
        for vtf in GenFdsGlobalVariable.FdfParser.profile.VtfList:
            compLocList = vtf.GetFvList()
            if set(compLocList).issubset(fvList):
                flag = True
                break
        if flag == True:
            self.vtfRawDict = vtf.GenVtf(fvAddDict)

        
##
# Create Flash Map file
##
    def GenFlashMap ():
        pass
##        FlashFile = open( os.path.join(GenFdsGlobalVariable.FvDir, 'FalshMap.h'), 'w+b')
##        FlashFile.writelines ("#ifndef _FLASH_MAP_H_" + T_CHAR_LF)
##        FlashFile.writelines ("#define _FLASH_MAP_H_" + T_CHAR_LF)
        
        



                
                
            
