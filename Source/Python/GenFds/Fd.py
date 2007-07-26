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
##        self.FdUiName = ''
##        self.CreateFileName = None
##        self.BaseAddress = None
##        self.BaseAddressPcd = None
##        self.Size = None
##        self.SizePcd = None
##        self.ErasePolarity = '1'
##        # 3-tuple list (blockSize, numBlocks, pcd)
##        self.BlockSizeList = []
##        # DefineVarDict[var] = value
##        self.DefineVarDict = {}
##        # SetVarDict[var] = value
##        self.SetVarDict = {}
##        self.RegionList = []
##        self.vtfRawDict = {}
        FDClassObject.__init__(self)
##
#  Create Fd file
##
    def GenFd (self, FvBinDict):
        #
        # Print Information
        #
        print 'Following Region will be add to Fd !!!'
        for item in GenFdsGlobalVariable.FdfParser.profile.FvDict:
            print item
            
        self.GenVtfFile()
        
        FdBuffer = StringIO.StringIO('')
        for Regions in self.RegionList :
            #
            # Call each region's AddToBuffer function 
            #
            Regions.AddToBuffer (FdBuffer, self.BaseAddress, self.BlockSizeList, self.ErasePolarity, FvBinDict, self.vtfRawDict)
        #
        # Create a empty Fd file
        #
        FdFileName = os.path.join(GenFdsGlobalVariable.FvDir,
                                  self.FdUiName + '.fd')
        fd = open(FdFileName, 'w+b')
       
        #
        # Write the buffer contents to Fd file
        #
        print "Fd File Name:%s" %FdFileName
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
                fvList.append(region.RegionData.upper())
                fvAddDict[region.RegionData.upper()] = (int(self.BaseAddress,16) + \
                                                region.Offset, region.Size)
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
        
        



                
                
            
