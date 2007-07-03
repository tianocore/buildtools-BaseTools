import GenFds
from struct import *
from GenFdsGlobalVariable import GenFdsGlobalVariable
import StringIO

class region:
    def __init__(self):
        self.Offset = None       # The begin position of the Region
        self.Size = None         # The Size of the Region
        self.PcdOffset = None
        self.PcdSize = None
        self.RegionSize = None
        self.SetVarDict = {}
        self.RegionType = None
        self.RegionData = None
        
        
        
##
#  Add RegionData to Fd file
##
    def AddToBuffer(self, Buffer, BlockSizeList, ErasePolarity, FvBinDict):
        Size = self.Size
        print "Fv Size = %d" %Size
        
        if self.RegionType == 'FV':
            #
            # Get Fv from FvDict
            #
            fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.RegionData.upper())
            #
            # Create local Buffer
            #
            
            if fv != None :
                print "GenFv: %s" %self.RegionData
                #
                # Call GenFv tool
                #
                BlockSize = self.__BlockSizeOfRegion__(BlockSizeList)
                BlockNum = self.__BlockNumOfRegion__(BlockSize)
                FvBaseAddress = '0x%x' %self.Offset
                FileName = fv.AddToBuffer(Buffer, FvBaseAddress, BlockSize, BlockNum, ErasePolarity)
                FvBinDict[self.RegionData.upper()] = FileName

        if self.RegionType == 'FILE':
            BinFile = open (self.RegionData, 'r+b')
            FvBuffer = StringIO.StringIO('')
            FvBuffer.write(BinFile.read())
            if FvBuffer.len > Size :
                raise Exception ("Size of File (%s) large than Region Size ", self.RegionData)
            #
            # If File contents less than region size, append "0xff" after it
            #
            elif FvBuffer.len < Size:
                for index in range(0, (Size-FvBuffer.len)):
                    if (ErasePolarity == '1'):
                        FvBuffer.write(Pack('B', int('0xFF', 16)))
                    else:
                        FvBuffer.write(Pack('B', int('0x00', 16)))
            Buffer.write(FvBuffer)
            FvBuffer.close()
            
        if self.RegionType == 'DATA' :
            Data = self.RegionData.split(',')
            if len(Data) > Size:
               raise Exception ("Size of DATA large than Region Size ")
            elif len(Data) <= Size:
                for item in Data :
                    Buffer.write(pack('B', int(item, 16)))
                for index in range(0, (Size - len(Data))):
                    if (ErasePolarity == '1'):
                        Buffer.write(pack('B', int('0xFF', 16)))
                    else:
                        Buffer.write(pack('B', int('0x00', 16)))
                
        if self.RegionType == None:
            for i in range(0, Size) :
                if (ErasePolarity == '1') :
                    Buffer.write(pack('B', int('0xFF', 16)))
                else :
                    Buffer.write(pack('B', int('0x00', 16)))

    def __BlockSizeOfRegion__(self, BlockSizeList):
        Offset = 0x00
        BlockSize = 0
        for item in BlockSizeList:
            Offset = Offset + item[0]  * item[1]
            print "Offset = 0x%x" %Offset
            print "self.Offset %x" %self.Offset
            if self.Offset < Offset :
                BlockSize = item[0]
                #print "BlockSize = %s" %BlockSize
                return BlockSize

    def __BlockNumOfRegion__ (self, BlockSize):
        BlockNum = self.Size / BlockSize
        #print "BlockNum = %x" %BlockNum
        return BlockNum
                
