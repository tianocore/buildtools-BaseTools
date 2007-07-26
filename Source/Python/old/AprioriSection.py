class AprioriSection :
    def __init__(self):
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        self.FfsList = []
        
    def GenFfs (self):
        FfsFileList = []
        for Ffs in self.FfsList :
            ffsFileName = Ffs.GenFfs ()
            FfsFileList.append(ffsFileName)
        return FfsFileList
            
            