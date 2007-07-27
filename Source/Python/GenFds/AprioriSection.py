from CommonDataClass.FdfClassObject import AprioriSectionClassObject
class AprioriSection (AprioriSectionClassObject):
    def __init__(self):
        AprioriSectionClassObject.__init__()
        
    def GenFfs (self):
        FfsFileList = []
        for Ffs in self.FfsList :
            ffsFileName = Ffs.GenFfs ()
            FfsFileList.append(ffsFileName)
        return FfsFileList
            
