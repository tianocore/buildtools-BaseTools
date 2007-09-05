import os
import subprocess
from Common import EdkLogger

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
    ActivePlatform = None

    def ExtendMarco (String):
        return String
    
    def SetDir (OutputDir, FdfParser, WorkSpace, ArchList):
        GenFdsGlobalVariable.VerboseLogger( "GenFdsGlobalVariable.OuputDir :%s" %OutputDir)
        GenFdsGlobalVariable.OuputDir = os.path.normpath(OutputDir)
        GenFdsGlobalVariable.FdfParser = FdfParser
        GenFdsGlobalVariable.WorkSpace = WorkSpace
        GenFdsGlobalVariable.FvDir = os.path.join(GenFdsGlobalVariable.OuputDir, 'Fv')
        GenFdsGlobalVariable.FfsDir = os.path.join(GenFdsGlobalVariable.FvDir, 'Ffs')
        if ArchList != None:
            GenFdsGlobalVariable.ArchList = ArchList
            
        if not os.path.exists(GenFdsGlobalVariable.FvDir) :
            os.makedirs(GenFdsGlobalVariable.FvDir)
        
    def SetDefaultRule (Rule) :
        GenFdsGlobalVariable.DefaultRule = Rule

    def ReplaceWorkspaceMarco(String):
        Str = String.replace('$(WORKSPACE)', GenFdsGlobalVariable.WorkSpaceDir)
        if os.path.exists(Str):
            Str = os.path.realpath(Str)
        else:
            Str = os.path.join(GenFdsGlobalVariable.WorkSpaceDir, String)
        return Str
    
    def CallExternalTool (cmd, errorMess):
        GenFdsGlobalVariable.InfLogger (cmd)
        #GenFdsGlobalVariable.VerboseLogger(cmd)
        PopenObject = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        (out, error) = PopenObject.communicate()

        while PopenObject.returncode == None :
            PopenObject.wait()
        if PopenObject.returncode != 0:
            GenFdsGlobalVariable.InfLogger ("Return Value = %d" %PopenObject.returncode)
            GenFdsGlobalVariable.InfLogger (out)
            GenFdsGlobalVariable.InfLogger (error)
            GenFdsGlobalVariable.InfLogger (errorMess)

    def VerboseLogger (msg):
        EdkLogger.verbose(msg)

    def InfLogger (msg):
        EdkLogger.info(msg)

    def DebugLogger (Level, msg):
        EdkLogger.debug(Level, msg)

    def MarcoExend (Str, MarcoDict):
        if Str == None :
            return None
        
        Dict = {'$(WORKSPACE)'   : GenFdsGlobalVariable.WorkSpaceDir}
        if MarcoDict != None  and len (MarcoDict) != 0:
            for marco in MarcoDict.keys():
                key = '$(' + marco + ')'
                Dict[key] = MarcoDict.get(marco)

        for key in Dict.keys():
            if Str.find(key) >= 0 :
                Str = Str.replace (key, Dict[key])
        return Str


    SetDir = staticmethod(SetDir)
    ExtendMarco = staticmethod(ExtendMarco)
    SetDefaultRule = staticmethod(SetDefaultRule)
    ReplaceWorkspaceMarco = staticmethod(ReplaceWorkspaceMarco)
    CallExternalTool = staticmethod(CallExternalTool)
    VerboseLogger = staticmethod(VerboseLogger)
    InfLogger = staticmethod(InfLogger)
    DebugLogger = staticmethod(DebugLogger)
    MarcoExend = staticmethod (MarcoExend)
