import GenFds
from struct import *
from GenFdsGlobalVariable import GenFdsGlobalVariable
import StringIO

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
        Size = int (self.Offset, 16) - int (self.Size, 16)
        if self.RegionType == 'FV':
            print "Find Region = %s in FvDict !!" %self.RegionData
            fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.RegionData.upper())
            FvBuffer = StringIO.StringIO('')
            if fv != None :
                print "Gen Fv"
                fv.AddToBuffer(FvBuffer, self.Offset)
                if FvBuffer.len() < Size :
                    Buffer.write(FvBuffer.getvalue())
                    index = 0
                    for index in range(Size - FvBuffer.len()):
                        Buffer.write(pack('B', int('0xFF', 16)))
            FvBuffer.close()
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
                
