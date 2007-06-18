import Section
class EfiSection (Section.Section):
    
    def __init__(self):
        
        self.SectionName = None
        self.Optional = False
        # store file name composed of MACROs
        self.Filename = None
        self.BuildNum = None
