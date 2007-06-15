class Section :
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
        'COMPRESS'  : 'EFI_SECTION_COMPRESSION'
    }
    ToolGuild = {
        '  '   :    'TianoCompress',
        '  '   :    'Laz7Compress',
        '  '   :    'CustomerCompress'
    }
    def __init__(self):
        self.Alignment = None
        
    def GenSection(self, OutputPath, GuidName):
        pass
