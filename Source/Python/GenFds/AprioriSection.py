from struct import *
import os
import StringIO
import FfsFileStatement
from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import AprioriSectionClassObject
from Common.String import *

class AprioriSection (AprioriSectionClassObject):
    
    def __init__(self):
        AprioriSectionClassObject.__init__(self)
        self.AprioriType = ""
        
    def GenFfs (self, fvName):
        DXE_GUID = "FC510EE7-FFDC-11D4-BD41-0080C73C8881"
        PEI_GUID = "1B45CC0A-156A-428A-AF62-49864DA0E6E6"
        Buffer = StringIO.StringIO('')
        guid = DXE_GUID
        if self.AprioriType == "PEI":
            guid = PEI_GUID
        OutputAprFilePath = os.path.join (GenFdsGlobalVariable.WorkSpaceDir, \
                                   GenFdsGlobalVariable.FfsDir,\
                                   guid + fvName)
        if not os.path.exists(OutputAprFilePath) :
            os.makedirs(OutputAprFilePath)
            
        OutputAprFileName = os.path.join( OutputAprFilePath, \
                                       guid + fvName + '.Apri' )
        AprFfsFileName = os.path.join (OutputAprFilePath,\
                                    guid + fvName + '.Ffs')
                                   
        OutputAprFile = open(OutputAprFileName, 'w+b')
        for ffs in self.FfsList :
            Guid = ""
            if isinstance(ffs, FfsFileStatement.FileStatements):
                Guid = ffs.NameGuid
            else:
                InfFileName = NormPath(ffs.InfFileName)
                Inf = GenFdsGlobalVariable.WorkSpace.Build['IA32'].ModuleDatabase.get(InfFileName)
                if Inf == None:
                    Inf = GenFdsGlobalVariable.WorkSpace.Build['X64'].ModuleDatabase.get(InfFileName)
                    if Inf == None:
                        Inf = GenFdsGlobalVariable.WorkSpace.Build['IPF'].ModuleDatabase.get(InfFileName)
                        if Inf == None:
                            Inf = GenFdsGlobalVariable.WorkSpace.Build['EBC'].ModuleDatabase.get(InfFileName)
                            if Inf == None:
                                raise Exception ("This File :%s doesn't exist!", InfFileName)
            
                Guid = Inf.Guid
            GuidPart = Guid.split('-')
            Buffer.write(pack('I', long(GuidPart[0], 16)))
            Buffer.write(pack('H', int(GuidPart[1], 16)))
            Buffer.write(pack('H', int(GuidPart[2], 16)))
            
            for Num in range(2):
                char = GuidPart[3][Num*2:Num*2+2]
                Buffer.write(pack('B', int(char, 16)))
            
            for Num in range(6):
                char = GuidPart[4][Num*2:Num*2+2]
                Buffer.write(pack('B', int(char, 16)))
    
        OutputAprFile.write(Buffer.getvalue())
        OutputAprFile.close()
        RawSectionFileName = os.path.join( OutputAprFilePath, \
                                       guid + fvName + '.raw' )
        
        GenSectionCmd = 'GenSec -o '                                     + \
                         RawSectionFileName                              + \
                         ' -s EFI_SECTION_RAW '                          + \
                         OutputAprFileName
        
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
        
        GenFfsCmd = 'GenFfs -t EFI_FV_FILETYPE_FREEFORM -g '         + \
                     guid                                            + \
                     ' -o '                                          + \
                     AprFfsFileName                                  + \
                     ' -i ' + RawSectionFileName
        
        
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd,"GenFfs Failed !")
        return AprFfsFileName
            
