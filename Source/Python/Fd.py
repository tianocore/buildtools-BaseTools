import Fd
import Region
import Fv

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
        self.BlockSizeList = None
        # DefineVarDict[var] = value
        self.DefineVarDict = None
        # SetVarDict[var] = value
        self.SetVarDict = None
        self.RegionList = None
        
        
##
#  Create Fd file
##
    def GenFd (FdPath):
        FdBuffer = StringIO(mode="a+b", bufsize="1024");
        for Regions in RegionList :
            #
            # Call each region's AddToBuffer function 
            #
            Regions.AddToBuffer (fd, self.BlockSizeList)
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
