from CommonDataClass.FdfClassObject import SectionClassObject

class Section (SectionClassObject):
    SectionType = {
        'RAW'       : 'EFI_SECTION_RAW',
        'FREEFORM'  : 'EFI_SECTION_FREEFORM_SUBTYPE_GUID',
        'PE32'      : 'EFI_SECTION_PE32',
        'PIC'       : 'EFI_SECTION_PIC',
        'TE'        : 'EFI_SECTION_TE',
        'FV_IMAGE'  : 'EFI_SECTION_FIRMWARE_VOLUME_IMAGE',
        'DXE_DEPEX' : 'EFI_SECTION_DXE_DEPEX',
        'PEI_DEPEX' : 'EFI_SECTION_PEI_DEPEX',
        'GUIDED'    : 'EFI_SECTION_GUID_DEFINED',
        'COMPRESS'  : 'EFI_SECTION_COMPRESSION',
        'UI'        : 'EFI_SECTION_USER_INTERFACE'
    }

    BinFileType = {
        'GUID'          : '.guid',
        'ACPI'          : '.acpi',
        'ASL'           : '.asl' ,
        'UEFI_APP'      : '.app',
        'LIB'           : '.lib',
        'PE32'          : '.pe32',
        'PIC'           : '.pic',
        'PEI_DEPEX'     : '.depex',
        'SEC_PEI_DEPEX' : '.depex',
        'TE'            : '.te',
        'UNI_VER'       : '.ver',
        'VER'           : '.ver',
        'UNI_UI'        : '.ui',
        'UI'            : '.ui',
        'BIN'           : '.bin',
        'RAW'           : '.raw',
        'COMPAT16'      : '.comp16',
        'FV'            : '.fv'
    }

    SectFileType = {
        'SEC_GUID'      : '.sec' ,
        'SEC_PE32'      : '.sec' ,
        'SEC_PIC'       : '.sec',
        'SEC_TE'        : '.sec',
        'SEC_VER'       : '.sec',
        'SEC_UI'        : '.sec',
        'SEC_COMPAT16'  : '.sec',
        'SEC_BIN'       : '.sec'
    }
    
    ToolGuild = {
        '0xa31280ad-0x481e-0x41b6-0x95e8-0x127f-0x4c984779' : 'TianoCompress',
        '0xee4e5898-0x3914-0x4259-0x9d6e-0xdc7b-0xd79403cf' : 'LzmaCompress'
    }
    def __init__(self):
        SectionClassObject.__init__(self)
        
    def GenSection(self, OutputPath, GuidName, SecNum, keyStringList, FfsInf = None):
        pass

    def GetFileList(FfsInf, FileType, FileExtension):
        if FileType in Section.SectFileType.keys() :
            IsSect = True
        else :
            IsSect = False
            
        if FileExtension != None:
            suffix = FileExtension
        elif IsSect :
            suffix = Section.SectionType[FileType]
        else:
            suffix = Section.BinFileType[FileType]
        if FfsInf == None:
            raise Exception ('Dont have Inf File!')
        
        FileList = []
        for File in FfsInf.BinFileList :
            if File.FileType == self.FileType:
                FileList.append(os.path.join(GenFdsGlobalVariable.WorkSpaceDir, FfsInf.SourceDir, File.BinaryFile))
            for file in os.listdir(FfsInf.EfiOutputPath):
                Name, Ext = os.path.splitext(file)
                if Ext == suffix:
                   FileList.append(FfsInf.EfiOutputPath, file)
                   
        return FileList, IsSect
    
    GetFileList = staticmethod(GetFileList)
