import Section
class FvImageSection(Section.Section):
    def __init__(self):
        self.Aligenment = None
        self.Fv = None
        
    def GenSection(self, OutputPath, ModuleName):
        buffer = StringIo(mode='a+')
        self.Fv.AddToBuffer(buffer)
        FvFileName = OutputPath + ModuleName + '.fv'
        FvFile = open ( FvFileName, mode ='w+')
        FvFile.write(buffer)
        FvFile.close()
        #
        # Prepare the parameter of GenSection
        #
        OutputFile = OutputPath + ModuleName + Ffs.SectionSuffix("FV_IMAGE")
        GenSectionCmd = 'GenSection -o ' + OutputFile + ' -s ' +  \
                        'EFI_SECTION_FIRMWARE_VOLUME_IMAGE ' + FvFileName
        popen (GenSectionCmd, mod ='r')
        
        return OutputFile
