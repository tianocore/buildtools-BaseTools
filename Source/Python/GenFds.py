from GenFdsGlobalVariable import GenFdsGlobalVariable

class GenFds :
    FdfParsef = None
    
    def GenFd (FvDir, BinDir, LibDir, FdfParser, WorkSpace):
        GenFdsGlobalVariable.SetDir (FvDir, BinDir, LibDir, FdfParser, WorkSpace)
        #GenFdsGlobalVariable.SetDefaultRule(None)
        
        for item in GenFdsGlobalVariable.FdfParser.profile.FdDict.keys():
            fd = GenFdsGlobalVariable.FdfParser.profile.FdDict[item]
            fd.GenFd()
    GenFd = staticmethod(GenFd)