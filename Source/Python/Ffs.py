class FFs:
    def __init__(self):
        self.NameGuid = None
        self.Fixed = False
        self.CheckSum = False
        self. Alignment = None
        self.SectionLsit = None
        
    def GenFfs():
        return ''
        
    def ModuleTypeToFileType(ModuleType):
        if (ModuleType == 'SEC'):
            return 'EFI_FV_FILETYPE_SECURITY_CORE'
        if (ModuleType == 'PEI_CORE'):
            return 'EFI_FV_FILETYPE_PEI_CORE'
        if (ModuleType == 'PEIM'):
            return 'EFI_FV_FILETYPE_PEIM'
        if (ModuleType == 'DXE_CORE'):
            return 'EFI_FV_FILETYPE_DXE_CORE'
        if (ModuleType == 'DXE_DRIVER'):
            return 'EFI_FV_FILETYPE_DRIVER'
        if (ModuleType == 'DXE_SAL_DRIVER'):
            return 'EFI_FV_FILETYPE_DRIVER'
        if (ModuleType == 'DXE_SMM_DRIVER'):
            return 'EFI_FV_FILETYPE_DRIVER'
        if (ModuleType == 'DXE_RUNTIME_DRIVER'):
            return 'EFI_FV_FIELTYPE_DRIVER'
        if (ModuleType == 'UEFI_DRIVER'):
            return 'EFI_FV_FILETYPE_DRIVER'
        if (ModuleType == 'UEFI_APPLICATION'):
            return 'EFI_FV_FILETYPE_APPLICATION'
        
    
    def SectionSuffix(sectionType):
        if SectionType == 'PE32':
            return '.pe32'
        if SectionType == 'PIC':
            return '.pic'
        if SectionType == 'TE':
            return '.te'
        if SectionType == 'DXE_DEPEX':
            return '.dpx'
        if SectionType == 'VERSION':
            return '.ver'
        if SectionType == 'UI' :
            return '.ui'
        if SectionType == 'COMPAT16':
            return '.com16'
        if SectionType == 'RAW':
            return '.raw'
        if SectionType == 'FREEFORM_SUBTYPE_GUID':
            return '.guid'
        if SectionType == 'FV_IMAGE':
            return 'fv.sec'

        
