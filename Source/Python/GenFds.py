from GenFdsGlobalVariable import GenFdsGlobalVariable

class GenFds :
    FdfParsef = None
    
    def GenFds(FvDir, BinDir, LibDir, FdfParser):
        GenFdsGlobalVariable.FvDir = FvDir
        GenFdsGlobalVariable.BinDir = BinDir
        GenFdsGlobalVariable.LibDir = LibDir
        GenFdsGlobalVariable.FdfParser = FdfParser
        

        for fd in GenFdsGlobalVariable.FdfParser.FdDict:
            fd.GenFds()
        