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
    ToolGuild = {
        '0xa31280ad-0x481e-0x41b6-0x95e8-0x127f-0x4c984779' : 'TianoCompress',
        '0xee4e5898-0x3914-0x4259-0x9d6e-0xdc7b-0xd79403cf' : 'LzmaCompress'
    }
    def __init__(self):

        #self.Alignment = None
        SectionClassObject.__init__(self)
        
    def GenSection(self, OutputPath, GuidName, keyStringList, FfsInf = None):
        pass
