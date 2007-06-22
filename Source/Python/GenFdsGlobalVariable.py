import os
class GenFdsGlobalVariable:
    FvDir = ''
    OuputDir = ''
    BinDir = ''
    FfsDir = ''      # FvDir + os.sep + 'Ffs'
    FdfParser = None
    LibDir = ''
    WorkSpace = None
    WorkSpaceDir = ''
    RuleDict = {}
    
    def ExtendMarco (String):
        return String
    
    def SetDir ():
        GenFdsGlobalVariable.FfsDir = GenFdsGlobalVariable.FvDir + os.sep + 'Ffs'
        GenFdsGlobalVariable.FfsDir = os.path.normpath(GenFdsGlobalVariable.FfsDir)
        GenFdsGlobalVariable.WorkSpaceDir = \
        GenFdsGlobalVariable.WorkSpace.Workspace.WorkspaceDir + \
        os.sep
        
    SetDir = staticmethod(SetDir)
        
    ExtendMarco = staticmethod(ExtendMarco)
