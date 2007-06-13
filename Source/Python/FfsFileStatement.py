class FileStatements ("parent: Ffs") :
    def __init__(self):
        self.FvType = None
        self.NameGuild = None
        self.Fixed = None
        self.Alignment = None
        self.SectionList = None
        
    def GenFfs():
        for section in self.SectionList :
            sectionFile, sectionAlignment = section.GenSection()
            sectionFileList.add(sectionFile, sectionAlignment)

