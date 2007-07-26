import Ffs
from GenFdsGlobalVariable import GenFdsGlobalVariable
import StringIO
class CapsuleData:
    def __init__(self):
       # self.FfsList = []
       # self.FvStatementList = []
        pass
    def GenCapsuleSubItem(self):
        pass
        

class CapsuleFfs (CapsuleData):
    def __init_(self) :
        self.Ffs = None

    def GenCapsuleSubItem(self):
        ffsFile = self.Ffs.GenFfs()
        return ffsFile

class CapsuleFv (CapsuleData):
    def __init__(self) :
        self.FvName = None

    def GenCapsuleSubItem(self):
        if self.FvName.find('.fv') != -1:
            if self.FvName in GenFdsGlobalVariable.FdfParser.profile.FvDict.keys():
                fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.FvName)
                FdBuffer = StringIO.StringIO('')
                FvFile = fv.AddToBuffer(FdBuffer)
                return FvFile
            
        else:
            FvFile = GenFdsGlobalVariable.ReplaceWorkspaceMarco(self.FvName)
            return FvFile
