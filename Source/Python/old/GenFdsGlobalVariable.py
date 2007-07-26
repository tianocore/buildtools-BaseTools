import os
import subprocess
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
    ArchList = None
    VtfDict = {}
    
    def ExtendMarco (String):
        return String
    
    def SetDir (OutputDir, FdfParser, WorkSpace, ArchList):
        print "GenFdsGlobalVariable.OuputDir :%s" %OutputDir
        GenFdsGlobalVariable.OuputDir = os.path.normpath(OutputDir)
        GenFdsGlobalVariable.FdfParser = FdfParser
        GenFdsGlobalVariable.WorkSpace = WorkSpace
        GenFdsGlobalVariable.FvDir = os.path.join(GenFdsGlobalVariable.OuputDir, 'Fv')
        GenFdsGlobalVariable.FfsDir = os.path.join(GenFdsGlobalVariable.FvDir, 'Ffs')
        GenFdsGlobalVariable.WorkSpaceDir = GenFdsGlobalVariable.WorkSpace.Workspace.WorkspaceDir
        if ArchList != None:
            GenFdsGlobalVariable.ArchList = ArchList
            
        if not os.path.exists(GenFdsGlobalVariable.FvDir) :
            os.makedirs(GenFdsGlobalVariable.FvDir)
            
    def SetDefaultRule (Rule) :
        GenFdsGlobalVariable.DefaultRule = Rule

    def ReplaceWorkspaceMarco(String):
        Str = String.replace('$(WORKSPACE)', GenFdsGlobalVariable.WorkSpaceDir)
        return Str
    
    def CallExternalTool (cmd, errorMess):
        PopenObject = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        (out, error) = PopenObject.communicate()

        while PopenObject.returncode == None :
            PopenObject.wait()
        if PopenObject.returncode != 0:
            print "Return Value = %d" %PopenObject.returncode
            print out
            print error
            raise Exception(errorMess)
        
    SetDir = staticmethod(SetDir)
    ExtendMarco = staticmethod(ExtendMarco)
    SetDefaultRule = staticmethod(SetDefaultRule)
    ReplaceWorkspaceMarco = staticmethod(ReplaceWorkspaceMarco)
    CallExternalTool = staticmethod(CallExternalTool)
