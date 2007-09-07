from struct import *
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import AprioriSectionClassObject
class AprioriSection (AprioriSectionClassObject):
    def __init__(self):
        AprioriSectionClassObject.__init__()
        DXE_GUID = ""
        PEI_GUID = ""
        
    def GenFfs (self):
        Buffer = StringIO.StringIO('')
        OutputFilePath = os.path.join (GenFdsGlobalVariable.WorkSpaceDir, \
                                   GenFdsGlobalVariable.FfsDir,\
                                   self.DXE_GUID)
        if not os.path.exists(OutputFilePath) :
            os.makedirs(OutputFilePath)
            
        OutputFileName = os.path.join( OutputFilePath, \
                                       Self.DXE_GUID + '.Apri' )
        FfsFileName = os.path.join (GenFdsGlobalVariable.WorkSpaceDir, \
                                    GenFdsGlobalVariable.FfsDir, \
                                    self.DXE_GUID,\
                                    self.DXE_GUID + '.Ffs')
                                   
        OutputFile = open(OutPutFileName, 'w+b')
        for Ffs in self.FfsList :
            Inf = GenFdsGlobalVariable.WorkSpace.Build['IA32'].ModuleDatabase.get(Ffs)
            if Inf == None:
                Inf = GenFdsGlobalVariable.WorkSpace.Build['IA64'].ModuleDatabase.get(Ffs)
            if Inf == None:
                Inf = GenFdsGlobalVariable.WorkSpace.Build['IPF'].ModuleDatabase.get(Ffs)
            if Inf == None:
                Inf = GenFdsGlobalVariable.WorkSpace.Build['EBC'].ModuleDatabase.get(Ffs)
            if Inf == None:
                raise Exception ("This File :%s doesn't exist!", Ffs)
            else:
                Guid = Inf.Header.Guid
                Guid = Guid.replace('-', '')
                for Num in range(0, 16):
                    char = Guid[Num*2:Num*2+2]
                    Buffer.write(pack('B', int(char, 16)))
        OutputFile.write(Buffer.getvalue())
        
        """Call GenFfs to GenFfsFile"""
        GenFfsCmd = 'GenFfs '                                     + \
                     ' -g '                                       + \
                     self.DXE_GUID                                + \
                     ' -o '                                       + \
                     FfsFileName                                  + \
                     ' '                                          + \
                     InputFile
                     
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd,"GenFfs Failed !")
        return FfsFileName
            
