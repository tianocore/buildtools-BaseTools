import sys
import os
import CodeFragmentCollector
import FileProfile
from CommonDataClass import DataClass
import Database
from Common import EdkLogger

def GetIgnoredDirList():
    return ('Build', 'IntelRestrictedPkg', 'IntelRestrictedTools')

def GetIdType(Str):
    Type = DataClass.MODEL_UNKNOWN
    Str = Str.replace('#', '# ')
    List = Str.split()
    if List[1] == 'include':
        Type = DataClass.MODEL_IDENTIFIER_INCLUDE
    elif List[1] == 'define':
        Type = DataClass.MODEL_IDENTIFIER_MACRO_DEFINE
    elif List[1] == 'ifdef':
        Type = DataClass.MODEL_IDENTIFIER_MACRO_IFDEF
    elif List[1] == 'ifndef':
        Type = DataClass.MODEL_IDENTIFIER_MACRO_IFNDEF
    elif List[1] == 'endif':
        Type = DataClass.MODEL_IDENTIFIER_MACRO_ENDIF
    elif List[1] == 'pragma':
        Type = DataClass.MODEL_IDENTIFIER_MACRO_PROGMA
    else:
        Type = DataClass.MODEL_UNKNOWN
    return Type

def GetIdentifierList():
    IdList = []
    for comment in FileProfile.CommentList:
        IdComment = DataClass.IdentifierClass(-1, '', '', '', comment.Content, DataClass.MODEL_IDENTIFIER_COMMENT, -1, -1, comment.StartPos[0],comment.StartPos[1],comment.EndPos[0],comment.EndPos[1])
        IdList.append(IdComment)
        
    for pp in FileProfile.PPDirectiveList:
        Type = GetIdType(pp.Content)
        IdPP = DataClass.IdentifierClass(-1, '', '', '', pp.Content, Type, -1, -1, pp.StartPos[0],pp.StartPos[1],pp.EndPos[0],pp.EndPos[1])
        IdList.append(IdPP)
        
    for pe in FileProfile.PredicateExpressionList:
        IdPE = DataClass.IdentifierClass(-1, '', '', '', pe.Content, DataClass.MODEL_IDENTIFIER_PREDICATE_EXPRESSION, -1, -1, pe.StartPos[0],pe.StartPos[1],pe.EndPos[0],pe.EndPos[1])
        IdList.append(IdPE)
        
    for var in FileProfile.VariableDeclarationList:
        for decl in var.Declarator.split(','):
            DeclList = decl.split('=')
            IdVar = DataClass.IdentifierClass(-1, var.Modifier, '', DeclList[0].strip(), (len(DeclList) > 1 and [DeclList[1]]or [''])[0], DataClass.MODEL_IDENTIFIER_VARIABLE, -1, -1, var.StartPos[0],var.StartPos[1],var.EndPos[0],var.EndPos[1])
            IdList.append(IdVar)
            
    for enum in FileProfile.EnumerationDefinitionList:
        LBPos = enum.Content.find('{')
        RBPos = enum.Content.find('}')
        Name = enum.Content[4:LBPos].strip()
        Value = enum.Content[LBPos+1:RBPos]
        IdEnum = DataClass.IdentifierClass(-1, '', '', Name, Value, DataClass.MODEL_IDENTIFIER_ENUMERATE, -1, -1, enum.StartPos[0],enum.StartPos[1],enum.EndPos[0],enum.EndPos[1])
        IdList.append(IdEnum)
        
    for su in FileProfile.StructUnionDefinitionList:
        Type = DataClass.MODEL_IDENTIFIER_STRUCTURE
        SkipLen = 6
        if su.Content.startswith('union'):
            Type = DataClass.MODEL_IDENTIFIER_UNION
            SkipLen = 5
        LBPos = su.Content.find('{')
        RBPos = su.Content.find('}')
        Name = su.Content[SkipLen:LBPos].strip()
        Value = su.Content[LBPos+1:RBPos]
        IdPE = DataClass.IdentifierClass(-1, '', '', Name, Value, Type, -1, -1, su.StartPos[0],su.StartPos[1],su.EndPos[0],su.EndPos[1])
        IdList.append(IdPE)
        
    for td in FileProfile.TypedefDefinitionList:
        IdTd = DataClass.IdentifierClass(-1, '', '', td.ToType, td.FromType, DataClass.MODEL_IDENTIFIER_TYPEDEF, -1, -1, td.StartPos[0],td.StartPos[1],td.EndPos[0],td.EndPos[1])
        IdList.append(IdTd)
        
    for funcCall in FileProfile.FunctionCallingList:
        IdFC = DataClass.IdentifierClass(-1, '', '', funcCall.FuncName, funcCall.ParamList, DataClass.MODEL_IDENTIFIER_FUNCTION_CALLING, -1, -1, funcCall.StartPos[0],funcCall.StartPos[1],funcCall.EndPos[0],funcCall.EndPos[1])
        IdList.append(IdFC)
    return IdList

def GetFunctionList():
    FuncObjList = []
    for FuncDef in FileProfile.FunctionDefinitionList:
        ParamIdList = []
        DeclSplitList = FuncDef.Declarator.split('(')
        if len(DeclSplitList) < 2:
            continue
        FuncName = DeclSplitList[0]
        ParamStr = DeclSplitList[1].rstrip(')')
        FuncNameLine = FuncDef.NamePos[0]
        FuncNameOffset = FuncDef.NamePos[1]
        LineSkipped = 0
        OffsetSkipped = 0
        Start = 0
        while FuncName.find('\n', Start) != -1:
            LineSkipped += 1
            OffsetSkipped = 0
            Start += FuncName.find('\n', Start)
            Start += 1       
        OffsetSkipped += len(FuncName[Start:])
        OffsetSkipped += 1 #skip '('
        ParamBeginLine = FuncNameLine + LineSkipped
        ParamBeginOffset = OffsetSkipped
        for p in ParamStr.split(','):
            ListP = p.split()
            if len(ListP) == 0:
                continue
            ParamName = ListP[-1]
            RightSpacePos = p.rfind(ParamName)
            ParamModifier = p[0:RightSpacePos]
            
            Start = 0
            while p.find('\n', Start) != -1:
                LineSkipped += 1
                OffsetSkipped = 0
                Start += p.find('\n', Start)
                Start += 1
            OffsetSkipped += len(p[Start:])
            
            ParamEndLine = ParamBeginLine + LineSkipped
            ParamEndOffset = OffsetSkipped
            IdParam = DataClass.IdentifierClass(-1, ParamModifier, '', ParamName, '', DataClass.MODEL_IDENTIFIER_PARAMETER, -1, -1, ParamBeginLine, ParamBeginOffset, ParamEndLine, ParamEndOffset)
            ParamIdList.append(IdParam)
            ParamBeginLine = ParamEndLine
            ParamBeginOffset = OffsetSkipped + 1 #skip ','
            
        FuncObj = DataClass.FunctionClass(-1, FuncDef.Declarator, FuncDef.Modifier, FuncName.strip(), '', FuncDef.StartPos[0],FuncDef.StartPos[1],FuncDef.EndPos[0],FuncDef.EndPos[1], FuncDef.LeftBracePos[0], FuncDef.LeftBracePos[1], -1, ParamIdList, [])
        FuncObjList.append(FuncObj)
        
    return FuncObjList

if __name__ == '__main__':

    FileObjList = []
    tuple = os.walk(sys.argv[1])

    ParseErrorFileList = []

    for dirpath, dirnames, filenames in tuple:
        for d in dirnames:
            if d.startswith('.') or d in GetIgnoredDirList():
                dirnames.remove(d)
        for f in filenames:
            FullName = os.path.join(dirpath, f)
            
            if os.path.splitext(f)[1] in ('.h', '.c'):
                print FullName
                model = f.endswith('c') and DataClass.MODEL_FILE_C or DataClass.MODEL_FILE_H
                collector = CodeFragmentCollector.CodeFragmentCollector(FullName)
                try:
                    collector.ParseFile()
                except:
                    ParseErrorFileList.append(FullName)
                    continue
#                collector.PrintFragments()
                BaseName = os.path.basename(f)
                DirName = os.path.dirname(FullName)
                Ext = os.path.splitext(f)[1].lstrip('.')
                ModifiedTime = os.path.getmtime(FullName)
                FileObj = DataClass.FileClass(-1, BaseName, Ext, DirName, FullName, model, ModifiedTime, GetFunctionList(), GetIdentifierList(), [])
                FileObjList.append(FileObj)
                collector.CleanFileProfileBuffer()   
    print ParseErrorFileList
    
    EdkLogger.Initialize()
    EdkLogger.SetLevel(EdkLogger.QUIET)
    Db = Database.Database(Database.DATABASE_PATH)
    Db.InitDatabase()
    Db.QueryTable(Db.TblDataModel)
    
    for file in FileObjList:    
        Db.InsertOneFile(file)

    Db.UpdateIdentifierBelongsToFunction()
    Db.Close()
        
    print 'Done!'
