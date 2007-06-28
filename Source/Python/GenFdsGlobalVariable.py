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
    DefaultRule = None
    
    def ExtendMarco (String):
        return String
    
    def SetDir (OutputDir, FdfParser, WorkSpace):
        print "GenFdsGlobalVariable.OuputDir :%s" %OutputDir
        GenFdsGlobalVariable.OuputDir = os.path.normpath(OutputDir)
        GenFdsGlobalVariable.FdfParser = FdfParser
        GenFdsGlobalVariable.WorkSpace = WorkSpace
        GenFdsGlobalVariable.FvDir = os.path.join(GenFdsGlobalVariable.OuputDir, 'Fv')
        GenFdsGlobalVariable.FfsDir = os.path.join(GenFdsGlobalVariable.FvDir, 'Ffs')
        GenFdsGlobalVariable.WorkSpaceDir = GenFdsGlobalVariable.WorkSpace.Workspace.WorkspaceDir
        
    def SetDefaultRule (Rule) :
        GenFdsGlobalVariable.DefaultRule = Rule

    SetDir = staticmethod(SetDir)
        
    ExtendMarco = staticmethod(ExtendMarco)
    SetDefaultRule = staticmethod(SetDefaultRule)
