import GenFds
from GenFdsGlobalVariable import GenFdsGlobalVariable

class region:
    def __init__(self):
        self.Offset = None
        self.Size = None
        self.PcdOffset = None
        self.PcdSize = None
        self.RegionSize = None
        self.SetVarDict = {}
        self.RegionType = None
        self.RegionData = None
        
        
        
##
#  Add RegionData to Fd file
##
    def AddToBuffer(self, Buffer, BlockSize):
        if self.RegionType == 'Fv':
            fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.RegionData)
            fv.InitialInf (BlockSize, self.Offset, self.Size)
            fv.AddToBuffer(Buffer)
        if self.RegionType == 'File':
            BinFile = open (self.RegionData, 'r')
            Buffer.write(BinFile.read())
        if self.RegionType == 'Data' :
            Buffer.write(self.RegionData)
