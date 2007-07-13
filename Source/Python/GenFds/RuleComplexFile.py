import Rule
class RuleComplexFile(Rule.Rule) :
    def __init__(self):
        Rule.Rule.__init__(self)
        self.SectionList = []