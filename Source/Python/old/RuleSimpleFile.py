import Rule
class RuleSimpleFile (Rule.Rule) :
    def __init__(self):
        Rule.Rule.__init__(self)
        self.FileName = None
        self.SectionType = ''
