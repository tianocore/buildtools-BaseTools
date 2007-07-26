import Rule
from CommonDataClass.FdfClassObject import RuleSimpleFileClassObject

class RuleSimpleFile (RuleSimpleFileClassObject) :
    def __init__(self):
##        Rule.Rule.__init__(self)
##        self.FileName = None
##        self.SectionType = ''
        RuleSimpleFileClassObject.__init__(self)
