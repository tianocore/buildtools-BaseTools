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
        Size = int (self.Size, 16)
        print "Fv Size = %d" %Size
        
        if self.RegionType == 'FV':
            #
            # Get Fv from FvDict
            #
            fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.RegionData.upper())
            #
            # Create local Buffer
            #
            FvBuffer = StringIO.StringIO('')
            
            if fv != None :
                print "GenFv: %s" %self.RegionData
                #
                # Call GenFv tool
                #
                fv.AddToBuffer(Buffer, self.Offset)
               
            
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
                    FvBuffer.write(Pack('B', int('0xFF', 16)))
            Buffer.write(FvBuffer)
            FvBuffer.close()
            
        if self.RegionType == 'DATA' :
            Data = self.RegionData.split(',')
            if Data.len > Size:
               raise Exception ("Size of DATA large than Region Size ")
            elif Data.len <= Size:
                for item in Data :
                    Buffer.write(pack('B', int(item, 16)))
                for index in range(0, (Size - Data.len)):
                    Buffer.write(pack('B'), int('0xFF', 16))
                
        if self.RegionType == None:
            for i in range(0, Size) :
                Buffer.write(pack('B', int('0xFF', 16)))
                
