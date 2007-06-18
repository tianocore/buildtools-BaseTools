import Rule
class RuleSimpleFile (Rule.Rule) :
    def __init__(self):
        self.Fixed = None
        self.CheckSum = None
        self.Alignment = None
        self.FileName = None
        self.FileModType = None
