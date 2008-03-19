import sys
import os
import re
import CodeFragmentCollector
import FileProfile
from CommonDataClass import DataClass
import Database
from Common import EdkLogger
from EccToolError import *
import EccGlobalData


def GetIgnoredDirListPattern():
    p = re.compile(r'.*[\\/](?:BUILD|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG|PCCTS)[\\/].*')
    return p

def GetFuncDeclPattern():
    p = re.compile(r'[^=]*\(.*\).*', re.DOTALL)
    return p

def GetDB():
    return EccGlobalData.gDb

def GetConfig():
    return EccGlobalData.gConfig

def PrintErrorMsg(ErrorType, Msg, TableName, ItemId):
    Msg = Msg.replace('\n', '').replace('\r', '')
    MsgPartList = Msg.split()
    Msg = ''
    for Part in MsgPartList:
        Msg += Part
        Msg += ' '
    GetDB().TblReport.Insert(ErrorType, OtherMsg = Msg, BelongsToTable = TableName, BelongsToItem = ItemId)

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
        
    FuncDeclPattern = GetFuncDeclPattern()
    for var in FileProfile.VariableDeclarationList:
        DeclText = var.Declarator.strip()
        while DeclText.startswith('*'):
            var.Modifier += '*'
            DeclText = DeclText.lstrip('*').strip()
        var.Declarator = DeclText
        if FuncDeclPattern.match(var.Declarator):
            IdVar = DataClass.IdentifierClass(-1, var.Modifier, '', var.Declarator, '', DataClass.MODEL_IDENTIFIER_FUNCTION_DECLARATION, -1, -1, var.StartPos[0],var.StartPos[1],var.EndPos[0],var.EndPos[1])
            IdList.append(IdVar)
            continue
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

def GetParamList(FuncDeclarator, FuncNameLine = 0, FuncNameOffset = 0):
    ParamIdList = []
    DeclSplitList = FuncDeclarator.split('(')
    if len(DeclSplitList) < 2:
        return None
    FuncName = DeclSplitList[0]
    ParamStr = DeclSplitList[1].rstrip(')')
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
        DeclText = ParamName.strip()
        RightSpacePos = p.rfind(ParamName)
        ParamModifier = p[0:RightSpacePos]
        if ParamName == 'OPTIONAL':
            if ParamModifier == '':
                ParamModifier += 'OPTIONAL'
                DeclText = ''
            else:
                ParamName = ListP[-2]
                DeclText = ParamName.strip()
                RightSpacePos = p.rfind(ParamName)
                ParamModifier = p[0:RightSpacePos]
                ParamModifier += 'OPTIONAL'
        while DeclText.startswith('*'):
            ParamModifier += '*'
            DeclText = DeclText.lstrip('*').strip()
        ParamName = DeclText
        
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
    
    return ParamIdList
    
def GetFunctionList():
    FuncObjList = []
    for FuncDef in FileProfile.FunctionDefinitionList:
        ParamIdList = []
        DeclText = FuncDef.Declarator.strip()
        while DeclText.startswith('*'):
            FuncDef.Modifier += '*'
            DeclText = DeclText.lstrip('*').strip()
        FuncDef.Declarator = DeclText
        DeclSplitList = FuncDef.Declarator.split('(')
        if len(DeclSplitList) < 2:
            continue
        
        FuncName = DeclSplitList[0]
        FuncObj = DataClass.FunctionClass(-1, FuncDef.Declarator, FuncDef.Modifier, FuncName.strip(), '', FuncDef.StartPos[0],FuncDef.StartPos[1],FuncDef.EndPos[0],FuncDef.EndPos[1], FuncDef.LeftBracePos[0], FuncDef.LeftBracePos[1], -1, ParamIdList, [])
        FuncObjList.append(FuncObj)
        
    return FuncObjList

def CollectSourceCodeDataIntoDB(RootDir):
    FileObjList = []
    tuple = os.walk(RootDir)
    IgnoredPattern = GetIgnoredDirListPattern()
    ParseErrorFileList = []

    for dirpath, dirnames, filenames in tuple:
        if IgnoredPattern.match(dirpath.upper()):
            continue
        for f in filenames:
            FullName = os.path.join(dirpath, f)
            
            if os.path.splitext(f)[1] in ('.h', '.c'):
                EdkLogger.info("Parsing " + FullName)
                model = f.endswith('c') and DataClass.MODEL_FILE_C or DataClass.MODEL_FILE_H
                collector = CodeFragmentCollector.CodeFragmentCollector(FullName)
                try:
                    collector.ParseFile()
                except UnicodeError:
                    ParseErrorFileList.append(FullName)
                    collector.CleanFileProfileBuffer()
                    collector.ParseFileWithClearedPPDirective()
#                collector.PrintFragments()
                BaseName = os.path.basename(f)
                DirName = os.path.dirname(FullName)
                Ext = os.path.splitext(f)[1].lstrip('.')
                ModifiedTime = os.path.getmtime(FullName)
                FileObj = DataClass.FileClass(-1, BaseName, Ext, DirName, FullName, model, ModifiedTime, GetFunctionList(), GetIdentifierList(), [])
                FileObjList.append(FileObj)
                collector.CleanFileProfileBuffer()   
    if len(ParseErrorFileList) > 0:
        EdkLogger.info("Found error during parsing:\n\t%s\n" % "\n\t".join(ParseErrorFileList))
    
    Db = GetDB()    
    for file in FileObjList:    
        Db.InsertOneFile(file)

    Db.UpdateIdentifierBelongsToFunction()

def CheckFuncHeaderDoxygenComments(FullFileName):
    ErrorMsgList = []
    Db = GetDB()
    
    SqlStatement = """ select ID
                       from File
                       where FullPath = '%s'
                   """ % FullFileName
    
    ResultSet = Db.TblFile.Exec(SqlStatement)
    FileTable = 'Identifier'
    FileID = -1
    for Result in ResultSet:
        FileTable += str(Result[0])
        if FileID != -1:
            ErrorMsgList.append('Duplicate file ID found in DB for file %s' % FullFileName)
            return ErrorMsgList
        FileID = Result[0]
    if FileID == -1:
        ErrorMsgList.append('NO file ID found in DB for file %s' % FullFileName)
        return ErrorMsgList
    
    SqlStatement = """ select Value, StartLine, EndLine, ID
                       from %s
                       where Model = %d
                   """ % (FileTable, DataClass.MODEL_IDENTIFIER_COMMENT)
    
    ResultSet = Db.TblFile.Exec(SqlStatement)
    CommentSet = []
    try:
        for Result in ResultSet:
            CommentSet.append(Result)
    except:
        print 'Unrecognized chars in comment'
    
    # Func Decl check
    SqlStatement = """ select Modifier, Name, StartLine, ID
                       from %s
                       where Model = %d
                   """ % (FileTable, DataClass.MODEL_IDENTIFIER_FUNCTION_DECLARATION)
    ResultSet = Db.TblFile.Exec(SqlStatement)
    for Result in ResultSet:
        FunctionHeaderComment = CheckCommentImmediatelyPrecedeFunctionHeader(Result[1], Result[2], CommentSet)
        if FunctionHeaderComment:
            CheckFunctionHeaderConsistentWithDoxygenComment(Result[0], Result[1], Result[2], FunctionHeaderComment[0], FunctionHeaderComment[1], ErrorMsgList, FunctionHeaderComment[3], FileTable)
        else:
            ErrorMsgList.append('Line %d :Function %s has NO comment immediately preceding it.' % (Result[2], Result[1]))
            PrintErrorMsg(ERROR_HEADER_CHECK_FUNCTION, 'Function %s has NO comment immediately preceding it.' % (Result[1]), FileTable, Result[3])
    
    # Func Def check
    SqlStatement = """ select Value, StartLine, EndLine, ID
                       from %s
                       where Model = %d
                   """ % (FileTable, DataClass.MODEL_IDENTIFIER_FUNCTION_HEADER)
    
    ResultSet = Db.TblFile.Exec(SqlStatement)
    CommentSet = []
    try:
        for Result in ResultSet:
            CommentSet.append(Result)
    except:
        print 'Unrecognized chars in comment'
    
    SqlStatement = """ select Modifier, Header, StartLine, ID
                       from Function
                       where BelongsToFile = %d
                   """ % (FileID)
    ResultSet = Db.TblFile.Exec(SqlStatement)
    for Result in ResultSet:
        FunctionHeaderComment = CheckCommentImmediatelyPrecedeFunctionHeader(Result[1], Result[2], CommentSet)
        if FunctionHeaderComment:
            CheckFunctionHeaderConsistentWithDoxygenComment(Result[0], Result[1], Result[2], FunctionHeaderComment[0], FunctionHeaderComment[1], ErrorMsgList, FunctionHeaderComment[3], FileTable)
        else:
            ErrorMsgList.append('Line %d :Function %s has NO comment immediately preceding it.' % (Result[2], Result[1]))
            PrintErrorMsg(ERROR_HEADER_CHECK_FUNCTION, 'Function %s has NO comment immediately preceding it.' % (Result[1]), 'Function', Result[3])
    return ErrorMsgList

def CheckCommentImmediatelyPrecedeFunctionHeader(FuncName, FuncStartLine, CommentSet):

    for Comment in CommentSet:
        if Comment[2] == FuncStartLine - 1:
            return Comment
    return None

def GetDoxygenStrFromComment(Str):
    DoxygenStrList = []
    ParamTagList = Str.split('@param')
    if len(ParamTagList) > 1:
        i = 1
        while i < len(ParamTagList):
            DoxygenStrList.append('@param' + ParamTagList[i])
            i += 1
        
    RetvalTagList = ParamTagList[-1].split('@retval')
    if len(RetvalTagList) > 1:
        if len(ParamTagList) > 1:
            DoxygenStrList[-1] = '@param' + RetvalTagList[0]
        i = 1
        while i < len(RetvalTagList):
            DoxygenStrList.append('@retval' + RetvalTagList[i])
            i += 1
    
    if len(DoxygenStrList) > 0:
        DoxygenStrList[-1] = DoxygenStrList[-1].rstrip('--*/')
    
    return DoxygenStrList
    
def CheckGeneralDoxygenCommentLayout(Str, StartLine, ErrorMsgList, CommentId = -1, TableName = ''):
    #/** --*/ @retval after @param
    if not Str.startswith('/**'):
        ErrorMsgList.append('Line %d : Comment does NOT have prefix /** ' % StartLine)
        PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'Comment does NOT have prefix /** ', TableName, CommentId)
    if not Str.endswith('**/'):
        ErrorMsgList.append('Line %d : Comment does NOT have tail **/ ' % StartLine)
        PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'Comment does NOT have tail **/ ', TableName, CommentId)
    FirstRetvalIndex = Str.find('@retval')
    LastParamIndex = Str.rfind('@param')
    if (FirstRetvalIndex > 0) and (LastParamIndex > 0) and (FirstRetvalIndex < LastParamIndex):
        ErrorMsgList.append('Line %d : @retval appear before @param ' % StartLine)
        PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'in Comment, @retval appear before @param  ', TableName, CommentId)
    
def CheckFunctionHeaderConsistentWithDoxygenComment(FuncModifier, FuncHeader, FuncStartLine, CommentStr, CommentStartLine, ErrorMsgList, CommentId = -1, TableName = ''):
    
    ParamList = GetParamList(FuncHeader) 
    CheckGeneralDoxygenCommentLayout(CommentStr, CommentStartLine, ErrorMsgList, CommentId, TableName)
    DoxygenStrList = GetDoxygenStrFromComment(CommentStr)
    DoxygenTagNumber = len(DoxygenStrList)
    ParamNumber = len(ParamList)
    Index = 0
    if ParamNumber > 0 and DoxygenTagNumber > 0:
        while Index < ParamNumber and Index < DoxygenTagNumber:
            ParamModifier = ParamList[Index].Modifier
            ParamName = ParamList[Index].Name.strip()
            Tag = DoxygenStrList[Index].strip(' ')
            if (not Tag[-1] == ('\n')) and (not Tag[-1] == ('\r')):
                ErrorMsgList.append('Line %d : in Comment, \"%s\" does NOT end with new line ' % (CommentStartLine, Tag.replace('\n', '').replace('\r', '')))
                PrintErrorMsg(ERROR_HEADER_CHECK_FUNCTION, 'in Comment, \"%s\" does NOT end with new line ' % (Tag.replace('\n', '').replace('\r', '')), TableName, CommentId)
            TagPartList = Tag.split()
            if len(TagPartList) < 2:
                ErrorMsgList.append('Line %d : in Comment, \"%s\" does NOT contain doxygen contents ' % (CommentStartLine, Tag.replace('\n', '').replace('\r', '')))
                PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'in Comment, \"%s\" does NOT contain doxygen contents ' % (Tag.replace('\n', '').replace('\r', '')), TableName, CommentId)
                Index += 1
                continue
            if Tag.find('[') > 0:
                InOutStr = ''
                ModifierPartList = ParamModifier.split()
                for Part in ModifierPartList:
                    if Part.strip() == 'IN':
                        InOutStr += 'in'
                    if Part.strip() == 'OUT':
                        if InOutStr != '':    
                            InOutStr += ', out'
                        else:
                            InOutStr = 'out'
                
                if InOutStr != '':
                    if Tag.find('['+InOutStr+']') == -1:
                        ErrorMsgList.append('Line %d : in Comment, \"%s\" does NOT have %s ' % (CommentStartLine, (TagPartList[0] + ' ' +TagPartList[1]).replace('\n', '').replace('\r', ''), '['+InOutStr+']'))    
                        PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'in Comment, \"%s\" does NOT have %s ' % ((TagPartList[0] + ' ' +TagPartList[1]).replace('\n', '').replace('\r', ''), '['+InOutStr+']'), TableName, CommentId)
            if Tag.find(ParamName) == -1 and ParamName != 'VOID' and ParamName != 'void':
                ErrorMsgList.append('Line %d : in Comment, \"%s\" does NOT consistent with parameter name %s ' % (CommentStartLine, (TagPartList[0] + ' ' +TagPartList[1]).replace('\n', '').replace('\r', ''), ParamName))    
                PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'in Comment, \"%s\" does NOT consistent with parameter name %s ' % ((TagPartList[0] + ' ' +TagPartList[1]).replace('\n', '').replace('\r', ''), ParamName), TableName, CommentId)
            Index += 1
        
        if Index < ParamNumber:
            ErrorMsgList.append('Line %d : Number of doxygen tags in comment less than number of function parameters' % CommentStartLine)
            PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'Number of doxygen tags in comment less than number of function parameters ', TableName, CommentId)
        if FuncModifier.find('VOID') != -1 or FuncModifier.find('void') != -1:
            if Index < DoxygenTagNumber - 1:
                ErrorMsgList.append('Line %d : Excessive doxygen tags in comment' % CommentStartLine)
                PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'Excessive doxygen tags in comment ', TableName, CommentId)
        else:
            if Index < DoxygenTagNumber and not DoxygenStrList[Index].startswith('@retval'): 
                ErrorMsgList.append('Line %d : Number of @param doxygen tags in comment does NOT match number of function parameters' % CommentStartLine)
                PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'Number of @param doxygen tags in comment does NOT match number of function parameters ', TableName, CommentId)
    else:
        if ParamNumber == 0 and DoxygenTagNumber != 0 and (FuncModifier.find('VOID') != -1 or FuncModifier.find('void') != -1):
            ErrorMsgList.append('Line %d : Excessive doxygen tags in comment' % CommentStartLine)
            PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'Excessive doxygen tags in comment ', TableName, CommentId)
        if ParamNumber != 0 and DoxygenTagNumber == 0:
            ErrorMsgList.append('Line %d : No doxygen tags in comment' % CommentStartLine)
            PrintErrorMsg(ERROR_DOXYGEN_CHECK_FUNCTION_HEADER, 'No doxygen tags in comment ', TableName, CommentId)

if __name__ == '__main__':

#    EdkLogger.Initialize()
#    EdkLogger.SetLevel(EdkLogger.QUIET)
#    CollectSourceCodeDataIntoDB(sys.argv[1])       
    MsgList = CheckFuncHeaderDoxygenComments('C:\\Combo\\R9\\LakeportX64Dev\\FlashDevicePkg\\Library\\SpiFlashChipM25P64\\SpiFlashChipM25P64.c')
    for Msg in MsgList:
        print Msg
    print 'Done!'
