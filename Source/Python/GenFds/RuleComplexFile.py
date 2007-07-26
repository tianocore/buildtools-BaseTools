import Rule
from  CommonDataClass.FdfClassObject import RuleComplexFileClassObject

class RuleComplexFile(RuleComplexFileClassObject) :
    def __init__(self):
##        Rule.Rule.__init__(self)
##        self.SectionList = []
        RuleComplexFileClassObject.__init__(self)
