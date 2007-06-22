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
    
    def SetDir (FvDir, BinDir, LibDir, FdfParser, WorkSpace):
        GenFdsGlobalVariable.FvDir = FvDir
        GenFdsGlobalVariable.BinDir = BinDir
        GenFdsGlobalVariable.LibDir = LibDir
        GenFdsGlobalVariable.FdfParser = FdfParser
        GenFdsGlobalVariable.WorkSpace = WorkSpace
        GenFdsGlobalVariable.FfsDir = GenFdsGlobalVariable.FvDir + os.sep + 'Ffs'
        GenFdsGlobalVariable.FfsDir = os.path.normpath(GenFdsGlobalVariable.FfsDir)
        GenFdsGlobalVariable.WorkSpaceDir = \
        GenFdsGlobalVariable.WorkSpace.Workspace.WorkspaceDir + \
        os.sep
        
    SetDir = staticmethod(SetDir)
        
    ExtendMarco = staticmethod(ExtendMarco)
