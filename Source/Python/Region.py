import GenFds
from struct import *
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
            fv.AddToBuffer(Buffer, self.Offset)
        if self.RegionType == 'File':
            BinFile = open (self.RegionData, 'r')
            Buffer.write(BinFile.read())
        if self.RegionType == 'Data' :
            Data = self.RegionData.split(',')
            for item in Data :
                Buffer.write(pack('B', int(item, 16)))
