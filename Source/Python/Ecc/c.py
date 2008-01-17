import sys
import os
import CodeFragmentCollector
import FileProfile
import CommonDataClass.DataClass as DataClass

for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for d in dirnames:
        if d.startswith('.'):
            dirnames.remove(d)
    for f in filenames:
        if os.path.splitext(f)[1] in ('.h', '.c'):
            collector = CodeFragmentCollector.CodeFragmentCollector(os.path.join(dirpath, f))
            collector.ParseFile()
            collector.PrintFragments()

#BaseName = os.path.basename(sys.argv[1])
#DirName = os.path.dirname(sys.argv[1])
#Ext = os.path.splitext(BaseName)[1]
#if Ext.startswith('.'):
#    Ext = Ext.lstrip('.')
#FileObj = DataClass.FileClass(Name = BaseName, ExtName = Ext, Path = DirName, FullPath = sys.argv[1])
#
#for func in FileProfile.FunctionDefinitionList:
#    FuncObj = DataClass.FunctionClass(Header = func.Declarator, Modifier = func.Modifier, Name = func.Declarator.split('(')[0].strip(), StartLine = func.StartPos[0], StartColumn = func.StartPos[1], EndLine = func.EndPos[0], EndColumn = func.EndPos[1])
#    FileObj.FunctionList.append(FuncObj)
#    
#for var in FileProfile.VariableDeclarationList:
#    VarObj = DataClass.VariableClass(Modifier = var.Modifier, Name = var.Declarator.split('=')[0].strip(), Value = (len(var.Declarator.split('=')) > 1 and [var.Declarator.split('=')[1]]or [''])[0], StartLine = var.StartPos[0], StartColumn = var.StartPos[1], EndLine = var.EndPos[0], EndColumn = var.EndPos[1])
#    FileObj.VariableList.append(VarObj)
    
print 'Done!'
