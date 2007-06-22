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
        self.ErasePolarity = False
        # 3-tuple list (blockSize, numBlocks, pcd)
        self.BlockSizeList = []
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        self.RegionList = []
        
        
##
#  Create Fd file
##
    def GenFd (self):
        FdBuffer = StringIO.StringIO('');
        for Regions in self.RegionList :
            #
            # Call each region's AddToBuffer function 
            #
            Regions.AddToBuffer (FdBuffer, self.BlockSizeList[0])
        #
        # Create a empty Fd file
        #
        fd = open(GenFdsGlobalVariable.FvDir + self.FdUiName + '.fd', 'w+b')
       
        #
        # Write the buffer contents to Fd file
        #
        fd.write(FdBuffer.getvalue());
        fd.close;
        FdBuffer.close;
        
##
# Create Flash Map file
##
    def GenFlashMap ():
        pass
