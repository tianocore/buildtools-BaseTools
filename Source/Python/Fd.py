import Region
import Fv
import os
import StringIO
import sys
from struct import *
from GenFdsGlobalVariable import GenFdsGlobalVariable
class FD:
    def __init__(self):
        self.FdUiName = ''
        self.CreateFileName = None
        self.BaseAddress = None
        self.BaseAddressPcd = None
        self.Size = None
        self.SizePcd = None
        self.ErasePolarity = '1'
        # 3-tuple list (blockSize, numBlocks, pcd)
        self.BlockSizeList = []
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        self.RegionList = []
        self.vtfRawDict = {}
        
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
        
##
# Create Flash Map file
##
    def GenFlashMap ():
        pass
    
    def GenVtfFile (self) :
        #
        # Get this Fd's all Fv name
        #
        fvAddDict ={}
        fvList = []
        for region in self.RegionList:
            if region.RegionType == 'FV':
                fvList.append(region.RegionData)
                fvAddDict[region.RegionData] = (int(self.BaseAddress,16) + \
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

        

               


                
                
            
