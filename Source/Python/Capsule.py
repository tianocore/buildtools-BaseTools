class Capsule :
    def __init__(self):
        self.SpecName = None
        self.UiCapsuleName = None
        self.CreatFile = None
        self.GroupIdNumber = None
#        self.DefineStatementList = None
#        self.SetSatementList = None
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        # TokensDict[var] = value
        self.TokensDict = {}
        self.CapsuleData = None
        