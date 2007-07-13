class Ffs:
    ModuleTypeToFileType = {
        'SEC'               : 'EFI_FV_FILETYPE_SECURITY_CORE',
        'PEI_CORE'          : 'EFI_FV_FILETYPE_PEI_CORE',
        'PEIM'              : 'EFI_FV_FILETYPE_PEIM',
        'DXE_CORE'          : 'EFI_FV_FILETYPE_DXE_CORE',
        'DXE_DRIVER'        : 'EFI_FV_FILETYPE_DRIVER',
        'DXE_SAL_DRIVER'    : 'EFI_FV_FILETYPE_DRIVER',
        'DXE_SMM_DRIVER'    : 'EFI_FV_FILETYPE_DRIVER',
        'DXE_RUNTIME_DRIVER': 'EFI_FV_FILETYPE_DRIVER',
        'UEFI_DRIVER'       : 'EFI_FV_FILETYPE_DRIVER',
        'UEFI_APPLICATION'  : 'EFI_FV_FILETYPE_APPLICATION'
    }
    FvTypeToFileType = {
        'SEC'               : 'EFI_FV_FILETYPE_SECURITY_CORE',
        'PEI_CORE'          : 'EFI_FV_FILETYPE_PEI_CORE',
        'PEIM'              : 'EFI_FV_FILETYPE_PEIM',
        'DXE_CORE'          : 'EFI_FV_FILETYPE_DXE_CORE',
        'FREEFORM'          : 'EFI_FV_FILETYPE_FREEFORM',
        'DRIVER'            : 'EFI_FV_FILETYPE_DRIVER',
        'APPLICATION'       : 'EFI_FV_FILETYPE_APPLICATION',
        'FV_IMAGE'          : 'EFI_FV_FILETYPE_FIRMWARE_VOLUME_IMAGE',
        'RAW'               : 'EFI_FV_FILETYPE_RAW',
        'PEI_DXE_COMBO'     : 'EFI_FV_FILETYPE_COMBINED_PEIM_DRIVER'
    }
    SectionSuffix = {
        'PE32'                 : '.pe32',
        'PIC'                  : '.pic',
        'TE'                   : '.te',
        'DXE_DEPEX'            : '.dpx',
        'VERSION'              : '.ver',
        'UI'                   : '.ui',
        'COMPAT16'             : '.com16',
        'RAW'                  : '.raw',
        'FREEFORM_SUBTYPE_GUID': '.guid',
        'FV_IMAGE'             : 'fv.sec',
        'COMPRESS'             : '.com',
        'GUIDED'               : '.guided',
        'PEI_DEPEX'            : '.dpx'
    }
    
    def __init__(self):
        self.NameGuid = None
        self.Fixed = False
        self.CheckSum = False
        self.Alignment = None
        self.SectionList = []
        
    def GenFfs():
        pass
