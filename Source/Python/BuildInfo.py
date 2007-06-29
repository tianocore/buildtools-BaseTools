class BuildInfo(object):
    def __init__(self, rawobj):
        self._Key = rawobj.DescFilePath

    def __str__(self):
        return self._Key

    def __eq__(self, other):
        return self._Key == str(other)

    def __hash__(self):
        return hash(self._Key)

class ModuleBuildInfo(BuildInfo):
    def __init__(self, module):
        BuildInfo.__init__(self, module)
        self.Module     = module

        self.Name       = module.BaseName
        self.Guid       = module.Guid
        self.Version    = module.Version
        self.ModuleType = module.ModuleType

        self.PlatformInfo = None
        self.PackageInfo = None
        self.Arch = ""
        self.ToolChain = ""
        self.BuildTarget = ""
        
        self.IsLibrary = False
        self.IsBinary = False

        self.BaseName = ""
        self.FileBase = ""
        self.FileExt = ""
        
        self.WorkspaceDir = ""
        self.SourceDir = ""
        self.BuildDir = ""
        self.OutputDir = ""
        self.DebugDir = ""
        self.MakefileDir = ""

        self.IncludePathList = []
        self.AutoGenFileList = []
        self.UnicodeFileList = []
        self.SourceFileList = []
        self.ObjectFileList = []

        self.DependentPackageList = []
        self.DependentLibraryList = []
        self.LibraryAutoGenList = []

        self.FileDependency = {}
        self.BuildOption = {}

        self.PcdList = []
        self.GuidList = []
        self.ProtocolList = []
        self.PpiList = []

        self.MacroList = []
        self.DepexList = []

class PackageBuildInfo(BuildInfo):
    def __init__(self, package):
        BuildInfo.__init__(self, package)
        self.Package    = package
        self.Name       = package.PackageName
        self.Guid       = package.Guid
        self.Version    = package.Version
        
        self.SourceDir = ""
        self.IncludePathList = []

class PlatformBuildInfo(BuildInfo):
    def __init__(self, platform):
        BuildInfo.__init__(self, platform)
        self.Platform   = platform
        self.Name       = platform.PlatformName
        self.Guid       = platform.Guid
        self.Version    = platform.Version

        self.ArchList = []
        self.ToolChain = ""
        self.BuildTarget = ""
        self.BuildRule = ""

        self.WorkspaceDir = ""
        self.SourceDir = ""
        self.BuildDir = ""
        self.OutputDir = ""
        self.DebugDir = ""
        self.LibraryDir = ""
        self.FvDir = ""
        self.MakefileDir = ""

        self.ModuleAutoGenList = []
        self.LibraryAutoGenList = []
        
        self.PcdTokenNumber = {}    # (TokenCName, TokenSpaceGuidCName) : GeneratedTokenNumber
        self.DynamicPcdList = []    # [(TokenCName1, TokenSpaceGuidCName1), (TokenCName2, TokenSpaceGuidCName2), ...]

        self.ToolPath = {}          # toolcode : tool path
        self.ToolDynamicLib = {}    # toolcode : lib path
        self.ToolStaticLib = {}     # toolcode : lib path
        self.ToolChainFamily = {}   # toolcode : tool chain family
        self.BuildOption = {}       # toolcode : option
        self.DefaultToolOption = {}
