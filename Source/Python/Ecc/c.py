import sys
import antlr3
from CLexer import CLexer
from CParser import CParser

from CodeFragmentCollector import CodeFragmentCollector
import FileProfile

collector = CodeFragmentCollector(sys.argv[1])
collector.PreprocessFile()
FileStringContents = ''
for fileLine in collector.Profile.FileLinesList:
    FileStringContents += fileLine
cStream = antlr3.StringStream(FileStringContents)
lexer = CLexer(cStream)
tStream = antlr3.CommonTokenStream(lexer)
parser = CParser(tStream)
parser.translation_unit()

for var in FileProfile.VariableDeclarationList:
    print str(var.StartPos) + var.Declarator
print 'Done!'
