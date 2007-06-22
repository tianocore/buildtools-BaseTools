from GenFdsGlobalVariable import GenFdsGlobalVariable

class GenFds :
    FdfParsef = None
    
    def GenFds(FvDir, BinDir, LibDir, FdfParser, WorkSpace):
        GenFdsGlobalVariable.FvDir = FvDir
        GenFdsGlobalVariable.BinDir = BinDir
        GenFdsGlobalVariable.LibDir = LibDir
        GenFdsGlobalVariable.FdfParser = FdfParser
        GenFdsGlobalVariable.WorkSpace = WorkSpace
        GenFdsGlobalVariable.SetFfsDir

        for fd in GenFdsGlobalVariable.FdfParser.FdDict:
            fd.GenFds()
        