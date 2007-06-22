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
        if self.RegionType == 'FV':
            fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.RegionData)
            fv.AddToBuffer(Buffer, self.Offset)
        if self.RegionType == 'FILE':
            BinFile = open (self.RegionData, 'r')
            Buffer.write(BinFile.read())
        if self.RegionType == 'DATA' :
            Data = self.RegionData.split(',')
            for item in Data :
                Buffer.write(pack('B', int(item, 16)))
        if self.RegionType == None:
            BegionRegion = int (self.Offset, 16)
            EndRegion = int(self.Size, 16)
            Size = EndRegion - BegionRegion
            print Size
            for i in range(0, Size) :
                Buffer.write(pack('B', int('0xFF', 16)))
                
