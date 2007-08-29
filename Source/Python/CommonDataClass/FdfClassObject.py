class FDClassObject:
    def __init__(self):
        self.FdUiName = ''
        self.CreateFileName = None
        self.BaseAddress = None
        self.BaseAddressPcd = None
        self.Size = None
        self.SizePcd = None
        self.ErasePolarity = '1'
        # 3-tuple list (blockSize, numBlocks, pcd)
        self.BlockSizeList = []
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        self.RegionList = []
        self.vtfRawDict = {}

class FvClassObject:
    def __init__(self):
        self.UiFvName = None
        self.CreateFileName = None
        # 3-tuple list (blockSize, numBlocks, pcd)
        self.BlockSizeList = []
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        self.FvAlignment = None
        # FvAttributeDict[attribute] = TRUE/FALSE (1/0)
        self.FvAttributeDict = {}
        self.AprioriSection = None
        self.FfsList = []
        self.BsBaseAddress = None
        self.RtBaseAddress = None

class RegionClassObject:
    def __init__(self):
        self.Offset = None       # The begin position of the Region
        self.Size = None         # The Size of the Region
        self.PcdOffset = None
        self.PcdSize = None
        self.RegionSize = None
        self.SetVarDict = {}
        self.RegionType = None
        self.RegionDataList = []
        
class FfsClassObject:
     def __init__(self):
        self.NameGuid = None
        self.Fixed = False
        self.CheckSum = False
        self.Alignment = None
        self.SectionList = []
        
class FileStatementsClassObject (FfsClassObject) :
    def __init__(self):
        FfsClassObject.__init__(self)
        self.FvType = None
        self.FileName = None
        self.KeyStringList = []
        self.FvName = None
        self.FdName = None
        self.DefineVarDict = {}
        self.AprioriSection = None

class FfsInfStatementClassObject(FfsClassObject):
    def __init__(self):
        FfsClassObject.__init__(self)
        self.Rule = None
        self.ver = None
        self.Ui = None
        self.InfFileName = None
        self.BuildNum = ''
        self.KeyStringList = []

class AprioriSectionClassObject:
    def __init__(self):
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        self.FfsList = []

        
class SectionClassObject:
    def __init__(self):
        self.Alignment = None
        
class CompressSectionClassObject (SectionClassObject) :
    def __init__(self):
        SectionClassObject.__init__(self)
        self.CompType = None
        self.SectionList = []
        
class DataSectionClassObject (SectionClassObject):
    def __init__(self):
        SectionClassObject.__init__(self)
        self.SecType = None
        self.SectFileName = None
        self.SectionList = []

class EfiSectionClassObject (SectionClassObject):

    def __init__(self):
        SectionClassObject.__init__(self)
        self.SectionType = None
        self.Optional = False
        self.FileType = None
        self.StringData = None
        self.FileName = None
        self.FileExtension = None
        self.BuildNum = None
        self.VersionNum = None
        
class FvImageSectionClassObject (SectionClassObject):
    def __init__(self):
        SectionClassObject.__init__(self)
        self.Fv = None
        self.FvName = None
        self.FvFileType = None
        self.FvFileName = None
        self.FvFileExtension = None
        
class GuidSectionClassObject (SectionClassObject) :
    def __init__(self):
        SectionClassObject.__init__(self)
        self.NameGuid = None
        self.SectionList = []
        self.SectionType = None
        self.ProcessRequired = False
        self.AuthStatusValid = False

class UiSectionClassObject (SectionClassObject):
    def __init__(self):
        SectionClassObject.__init__(self)
        self.StringData = None
        self.FileName = None
        
class VerSectionClassObject (SectionClassObject):
    def __init__(self):
        SectionClassObject.__init__(self)
        self.BuildNum = None
        self.StringData = None
        self.FileName = None

class RuleClassObject :
    def __init__(self):
        self.Arch = None
        self.ModuleType = None    # For Module Type
        self.TemplateName = None
        self.NameGuid = None
        self.Fixed = False
        self.Alignment = None
        self.CheckSum = False
        self.FvType = None       # for Ffs File Type
        self.KeyStringList = []
        
class RuleComplexFileClassObject(RuleClassObject) :
    def __init__(self):
        RuleClassObject.__init__(self)
        self.SectionList = []

class RuleSimpleFileClassObject(RuleClassObject) :
    def __init__(self):
        RuleClassObject.__init__(self)
        self.FileName = None
        self.SectionType = ''

class RuleFileExtensionClassObject(RuleClassObject):
    def __init__(self):
        RuleClassObject.__init__(self)
        self.FileExtension = None
        
class CapsuleClassObject :
    def __init__(self):
        self.SpecName = None
        self.UiCapsuleName = None
        self.CreateFile = None
        self.GroupIdNumber = None
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        # TokensDict[var] = value
        self.TokensDict = {}
        self.CapsuleDataList = []

class VtfClassObject :
    def __init__(self):
        self.KeyArch = None
        self.ArchList = None
        self.UiName = None
        self.ResetBin = None
        self.ComponentStatementList = []
        
class ComponentStatementClassObject :
    def __init__(self):
        self.CompName = None
        self.CompLoc = None
        self.CompType = None
        self.CompVer = None
        self.CompCs = None
        self.CompBin = None
        self.CompSym = None
        self.CompSize = None
        
        
##class UefiTokenClassObject:
##    def __init__(self):
##        self.CapsuleGuid = None
##        self.CapsuleHeaderSize = None
##        self.CapsuleFlags = None
##
##class FrameworkTokenClassObject :
##    def __init__(self):
##        self.SequenceNumber = None
##        self.InstanceId = None
##        self.ToSplitInfo = None
##        self.ToCapsuleBody = None
##        self.ToAuthorInfo = None
##        self.ToRevisionInfo = None
##        self.ToShortDesc = None
##        self.ToLongDesc = None
##        self.ToApplicatebleDevices = None