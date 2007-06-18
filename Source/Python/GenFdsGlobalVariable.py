import os
class GenFdsGlobalVariable:
    FvDir = ''
    OuputDir = ''
    BinDir = ''
    FfsDir = ''      # FvDir + os.sep + 'Ffs'
    FdfParser = None
    LibDir = ''
    
    
    def ExtendMarco (String):
        return String
    
    ExtendMarco = staticmethod(ExtendMarco)
