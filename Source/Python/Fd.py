import Fd
import Region
import Fv
import os
import StringIO
class FD:
    def __init__(self):
        self.FdUiName = None
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
    def GenFd (self, FdPath):
        FdBuffer = StringIO.StringIO('');
        for Regions in self.RegionList :
            #
            # Call each region's AddToBuffer function 
            #
            Regions.AddToBuffer (FdBuffer, self.BlockSizeList[0])
        #
        # Create a empty Fd file
        #
        if  not (FdPath.endswith ('/', start=0, end = sys.maxint)) or \
            not (FdPath.endswith ('\\', start=0, end = sys.maxint)) :
            fd = open(FdPath + Os.sep + file.self.FdUiName, mode='w+b')
        else :
            fd = open(FdPath + file.self.FdUiName, mode='w+b')
        #
        # Write the buffer contents to Fd file
        #
        fd.write(FdBuffer);
        FdBuffer.close;
        fd.close;
        
##
# Create Flash Map file
##
    def GenFlashMap ():
        pass
