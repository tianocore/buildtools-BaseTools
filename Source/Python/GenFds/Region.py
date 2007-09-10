from struct import *
from GenFdsGlobalVariable import GenFdsGlobalVariable
import StringIO
from CommonDataClass.FdfClassObject import RegionClassObject
import os
class region(RegionClassObject):
    def __init__(self):
        RegionClassObject.__init__(self)
        

    """Add RegionData to Fd file"""

    def AddToBuffer(self, Buffer, BaseAddress, BlockSizeList, ErasePolarity, FvBinDict, vtfDict = None, MarcoDict = None):
        Size = self.Size
        GenFdsGlobalVariable.InfLogger('Generate Region')
        GenFdsGlobalVariable.InfLogger("   Region Size = %d" %Size)
        GenFdsGlobalVariable.SharpCounter = 0
        
        if self.RegionType == 'FV':
            #
            # Get Fv from FvDict
            #
            FvBuffer = StringIO.StringIO('')
            BlockSize = self.__BlockSizeOfRegion__(BlockSizeList)
            if len(self.RegionDataList) == 1:
                RegionData = self.RegionDataList[0]
                fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(RegionData.upper())
            #
            # Create local Buffer            #
            
                if fv != None :
                    GenFdsGlobalVariable.InfLogger('   Region Name = FV')
                    #
                    # Call GenFv tool
                    #
                
                    self.FvAddress = int(BaseAddress, 16) + self.Offset
                    BlockSize = self.__BlockSizeOfRegion__(BlockSizeList)
                    BlockNum = self.__BlockNumOfRegion__(BlockSize)
                    FvBaseAddress = '0x%x' %self.FvAddress
                    FileName = fv.AddToBuffer(FvBuffer, FvBaseAddress, BlockSize, BlockNum, ErasePolarity, vtfDict)
                    
                    #BinFile = open (FileName, 'r+b')
                    #FvBuffer.write(BinFile.read())
                    FvBinDict[self.RegionDataList[0].upper()] = FileName
            else:
                for RegionData in self.RegionDataList:
                    fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(RegionData.upper())
                    if fv != None:
                        FileName = fv.AddToBuffer(FvBuffer, None, BlockSize, None, ErasePolarity, vtfDict)
                        FvBinDict[RegionData.upper()] = FileName
                
            if FvBuffer.len > Size:
                raise Exception ("Size of Region (%s) is large than Region Size ", self.Offset)
            elif FvBuffer.len < Size :
                raise Exception ("Size of Region (%s) is less than Region Size ", self.Offset)

            #BinFile = open (FileName, 'r+b')
            #Buffer.write(BinFile.read())
            Buffer.write(FvBuffer.getvalue())
            FvBuffer.close()

        if self.RegionType == 'FILE':
            FvBuffer = StringIO.StringIO('')
            for RegionData in self.RegionDataList:
                RegionData = GenFdsGlobalVariable.MarcoExend(RegionData, MarcoDict)
                GenFdsGlobalVariable.InfLogger('   Region File Name = FILE: %s'%RegionData)
                if RegionData[1] != ':' :
                    RegionData = os.path.join (GenFdsGlobalVariable.WorkSpaceDir, RegionData)
                if not os.path.exists(RegionData):
                    raise Exception ( 'File: %s dont exist !' %RegionData)
                
                BinFile = open (RegionData, 'r+b')
                FvBuffer.write(BinFile.read())
                if FvBuffer.len > Size :
                    raise Exception ("Size of File (%s) large than Region Size ", RegionData)

            #
            # If File contents less than region size, append "0xff" after it
            #
            if FvBuffer.len < Size:
                for index in range(0, (Size-FvBuffer.len)):
                    if (ErasePolarity == '1'):
                        FvBuffer.write(pack('B', int('0xFF', 16)))
                    else:
                        FvBuffer.write(pack('B', int('0x00', 16)))
            Buffer.write(FvBuffer.getvalue())
            FvBuffer.close()
            
        if self.RegionType == 'DATA' :
            GenFdsGlobalVariable.InfLogger('   Region Name = DATA')
            DataSize = 0
            for RegionData in self.RegionDataList:
                Data = RegionData.split(',')
                DataSize = DataSize + len(Data)
                if DataSize > Size:
                   raise Exception ("Size of DATA large than Region Size ")
                else:
                    for item in Data :
                        Buffer.write(pack('B', int(item, 16)))
            if DataSize < Size:
                if (ErasePolarity == '1'):
                    Buffer.write(pack(str(Size -DataSize)+'B', *(int('0xFF', 16) for i in range(Size - DataSize))))
                else:
                    Buffer.write(pack(str(Size - DataSize)+'B', *(int('0x00', 16) for i in range(Size - DataSize))))

                
        if self.RegionType == None:
            GenFdsGlobalVariable.InfLogger('   Region Name = None')
            if (ErasePolarity == '1') :
                Buffer.write(pack(str(Size)+'B', *(int('0xFF', 16) for i in range(0, Size))))
            else :
                Buffer.write(pack(str(Size)+'B', *(int('0x00', 16) for i in range(0, Size))))

    def __BlockSizeOfRegion__(self, BlockSizeList):
        Offset = 0x00
        BlockSize = 0
        for item in BlockSizeList:
            Offset = Offset + item[0]  * item[1]
            GenFdsGlobalVariable.VerboseLogger ("Offset = 0x%x" %Offset)
            GenFdsGlobalVariable.VerboseLogger ("self.Offset %x" %self.Offset)

            if self.Offset < Offset :
                BlockSize = item[0]
                GenFdsGlobalVariable.VerboseLogger ("BlockSize = %s" %BlockSize)
                return BlockSize
        return BlockSize
    
    def __BlockNumOfRegion__ (self, BlockSize):
        if BlockSize == 0 :
            raise Exception ("Region: %s doesn't in Fd address scope !" %self.Offset)
        BlockNum = self.Size / BlockSize
        GenFdsGlobalVariable.VerboseLogger ("BlockNum = %x" %BlockNum)
        return BlockNum
                
