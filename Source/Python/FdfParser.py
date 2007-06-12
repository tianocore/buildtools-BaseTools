import Fd
import Region

#define T_CHAR_SPACE                ' '
#define T_CHAR_NULL                 '\0'
#define T_CHAR_CR                   '\r'
#define T_CHAR_TAB                  '\t'
#define T_CHAR_LF                   '\n'
#define T_CHAR_SLASH                '/'
#define T_CHAR_BACKSLASH            '\\'
#define T_CHAR_DOUBLE_QUOTE         '\"'
#define T_CHAR_SINGLE_QUOTE         '\''
#define T_CHAR_STAR                 '*'
#define T_CHAR_HASH                 '#'

(T_CHAR_SPACE, T_CHAR_NULL, T_CHAR_CR, T_CHAR_TAB, T_CHAR_LF, T_CHAR_SLASH, \
T_CHAR_BACKSLASH, T_CHAR_DOUBLE_QUOTE, T_CHAR_SINGLE_QUOTE, T_CHAR_STAR, T_CHAR_HASH) = \
(' ', '\0', '\r', '\t', '\n', '/', '\\', '\"', '\'', '*', '#')

def Warning(s):
    print s + '\n'

class FileProfile :
    """File image in memory and information retrieved from it"""
    def __init__(self, filename):
        try:
            fsock = open(filename, "rb", 0)
            try:
                self.FileLinesList = []
                self.FileLinesList = fsock.readlines()
            finally:
                fsock.close()

        except IOError:
            print "Error when opening file."
            return
        
        #FileBufferPos = [CurrentLineNumber - 1, CurrentOffsetWithinLine]

        #self.DictVarNameValue = {}
        #self.DictPcdNameValue = {}
        self.FdDict = {}
        
class FdfParser :
    

    def __init__(self, filename):
        self.profile = FileProfile(filename)
        self.CurrentLineNumber = 1
        self.CurrentOffsetWithinLine = 0
        self.__Token = ""
        self.__ParserBreak = False

    """Whether char at current FileBufferPos is whitespace,"""
    def __IsWhiteSpace(self, char):
        if char in (T_CHAR_NULL, T_CHAR_CR, T_CHAR_SPACE, T_CHAR_TAB, T_CHAR_LF):
            return True
        else:
            return False

    """Skip white spaces from current char, return number of chars skipped"""
    def __SkipWhiteSpace(self):
        Count = 0
        while not self.__EndOfFile(self):
            Count += 1
            CurrentLineLen = len(self.profile.FileLinesList[self.CurrentLineNumber-1])
            if self.__CurrentChar(self) in (T_CHAR_NULL, T_CHAR_CR, T_CHAR_SPACE, T_CHAR_TAB):
                self.__GetOneChar(self)
            if self.__CurrentChar(self) == T_CHAR_LF:
                self.CurrentLineNumber += 1
                self.CurrentOffsetWithinLine = 0
            else:
                return Count - 1

    """Judge current buffer pos is at file end"""
    def __EndOfFile(self):
        NumberOfLines = len(profile.FileLinesList)
        SizeOfLastLine = len(profile.FileLinesList[-1])
        if self.CurrentLineNumber == NumberOfLines and self.CurrentOffsetWithinLine >= SizeOfLastLine - 1:
            return True
        else:
            return False

    """Judge current char is at line end"""
    def __EndOfLine(self):
        SizeOfCurrentLine = len(profile.FileLinesList[self.CurrentLineNumber - 1])
        if self.CurrentOffsetWithinLine >= SizeOfCurrentLine - 1:
            return True
        else:
            return False
    
    """Reset file data buffer to the initial state"""
    def Rewind(self):
        self.CurrentLineNumber = 1
        self.CurrentOffsetWithinLine = 0
        
    def __UndoOneChar(self):
        
        if self.CurrentLineNumber == 1 and self.CurrentOffsetWithinLine == 0:
            return False
        elif self.CurrentOffsetWithinLine == 0:
            self.CurrentLineNumber -= 1
            self.CurrentOffsetWithinLine = len(self.__CurrentLine(self)) - 1
        else:
            self.CurrentLineNumber -= 1
            self.CurrentOffsetWithinLine -= 1
        return True
        
    """Forward one char"""
    def __GetOneChar(self):
        if self.CurrentOffsetWithinLine == len(self.profile.FileLinesList[self.CurrentLineNumber - 1]) - 1:
                self.CurrentLineNumber += 1
                self.CurrentOffsetWithinLine = 0
        else:
                self.CurrentOffsetWithinLine += 1

    """Return copy of current char"""
    def __CurrentChar(self):
        return self.profile.FileLinesList[self.CurrentLineNumber - 1][self.CurrentOffsetWithinLine]
    
    """Return copy of next char"""
    def __NextChar(self):
        if self.CurrentOffsetWithinLine == len(self.profile.FileLinesList[self.CurrentLineNumber - 1]) - 1:
            return self.profile.FileLinesList[self.CurrentLineNumber][0]
        else:
            return self.profile.FileLinesList[self.CurrentLineNumber - 1][self.CurrentOffsetWithinLine + 1]
        
    """Modify the value of current char"""
    def __SetCurrentCharValue(self, value):
        self.profile.FileLinesList[self.CurrentLineNumber - 1][self.CurrentOffsetWithinLine] = value
        
    """Get current file line"""
    def __CurrentLine(self):
        return self.profile.FileLinesList[self.CurrentLineNumber - 1]
        
    """Replace comments with spaces"""
    def PreprocessFile(self):
        # change string to list of chars, as string can NOT be modified
        self.profile.FileLinesList = [list(s) for s in self.profile.FileLinesList]

        Rewind(self)
        InComment = False
        DoubleSlashComment = False
        HashComment = False

        while not self.__EndOfFile(self):
            
            # meet new line, then no longer in a comment for // and '#'
            if self.__CurrentChar(self) == T_CHAR_LF:
                self.CurrentLineNumber += 1
                self.CurrentOffsetWithinLine = 0
                if InComment and DoubleSlashComment:
                    InComment = False
                    DoulbeSlashComment = False
                if InComment and HashComment:
                    InComment = False
                    HashComment = False
            # check for */ comment end
            elif InComment and not DoubleSlashComment and not HashComment and self.__CurrentChar(self) == T_CHAR_STAR and self.__NextChar(self) == T_CHAR_SLASH:
                self.__SetCurrentCharValue(self, T_CHAR_SPACE)
                self.__GetOneChar(self)
                self.__SetCurrentCharValue(self, T_CHAR_SPACE)
                self.__GetOneChar(self)
                InComment = False
            # set comments to spaces
            elif InComment:
                self.__SetCurrentCharValue(self, T_CHAR_SPACE)
                self.__GetOneChar(self)
            # check for // comment
            elif self.__CurrentChar(self) == T_CHAR_SLASH and self.__NextChar(self) == T_CHAR_SLASH and not self.__EndOfLine(self):
                InComment = True
                DoubleSlashComment = True
            # check for '#' comment
            elif self.__CurrentChar(self) == T_CHAR_HASH and not self.__EndOfLine(self):
                InComment = True
                HashComment = True
            # check for /* comment start
            elif self.__CurrentChar(self) == T_CHAR_SLASH and self.__NextChar(self) == T_CHAR_STAR:
                self.__SetCurrentCharValue(self, T_CHAR_SPACE)
                self.__GetOneChar(self)
                self.__SetCurrentCharValue(self, T_CHAR_SPACE)
                self.__GetOneChar(self)
                InComment = True
            else:
                self.__GetOneChar(self)

        # restore from ListOfList to ListOfString
        self.profile.FileLinesList = ["".join(list) for list in self.profile.FileLinesList]
        Rewind(self)

    """check whether input string is found from current char position along"""
    def __IsToken(self, string):
        self.__SkipWhiteSpace(self)
        if self.__EndOfFile(self):
            return False
        # Only consider the same line, no multi-line token allowed
        index = self.__CurrentLine(self)[self.CurrentOffsetWithinLine, -1].find(string)
        if index == 0:
            self.CurrentOffsetWithinLine += len(string)
            return True
        return False

    """check whether input keyword is found from current char position along, whole word only!"""
    def __IsKeyword(self, keyword):
        self.__SkipWhiteSpace(self)
        if self.__EndOfFile(self):
            return False
        # Only consider the same line, no multi-line token allowed
        index = self.__CurrentLine(self)[self.CurrentOffsetWithinLine, -1].find(keyword)
        if index == 0:
            if not str(self.__CurrentLine(self)[self.CurrentOffsetWithinLine + len(keyword)]).isspace() and \
            self.__CurrentLine(self)[self.CurrentOffsetWithinLine + len(keyword)] != '=':
                return False
            self.CurrentOffsetWithinLine += len(keyword)
            return True
        return False

    """get next C name from file lines"""
    def __GetNextWord(self):
        self.__SkipWhiteSpace(self)
        if self.__EndOfFile(self):
            return False
        
        TempChar = self.__CurrentChar(self)
        StartPos = self.CurrentOffsetWithinLine
        if (TempChar >= 'a' and TempChar <= 'z') or (TempChar >= 'A' and TempChar <= 'Z') or TempChar == '_':
            self.__GetOneChar(self)
            while not self.__EndOfFile(self):
                TempChar = self.__CurrentChar(self)
                if (TempChar >= 'a' and TempChar <= 'z') or (TempChar >= 'A' and TempChar <= 'Z') \
                or (TempChar >= '0' and TempChar <= '9') or TempChar == '_' or TempChar == '-':
                    self.__GetOneChar(self)
                    
                else:
                    break

            self.Token = self.__CurrentLine[StartPos, self.CurrentOffsetWithinLine]
            return True
        #elif ...:
            # other conditions
        #    return True
            
        return False
    
    def __GetNextToken(self):
        self.__SkipWhiteSpace(self)
        if self.__EndOfFile(self):
            return False

        while not self.__EndOfFile(self):
                TempChar = self.__CurrentChar(self)
                if not str(TempChar).isspace():
                    self.__GetOneChar(self)
                else:
                    break
        else:
            return False
        
        self.Token = self.__CurrentLine[StartPos, self.CurrentOffsetWithinLine]
        return True

    def __UndoToken(self):
        while self.__UndoOneChar(self) and not str(self.__CurrentChar(self)).isspace():
            pass
    
    def __HexDigit(self, TempChar):
        if (TempChar >= 'a' and TempChar <= 'f') or (TempChar >= 'A' and TempChar <= 'F') \
                or (TempChar >= '0' and TempChar <= '9'):
                    return True
        else:
            return False
        
    def __GetHexNumber(self):
        if not self.__GetNextToken(self):
            return False
        if not self.Token.startswith("0x"):
            return False
        if len(self.Token) <= 2:
            return False
        charList = [c for c in self.Token[2, -1] if not self.__HexDigit(self, c)]
        if len(charList) == 0:
            return True
        else:
            return False
        
    def __GetDecimalNumber(self):
        if not self.__GetNextToken(self):
            return False
        if self.Token.isdigit():
            return True
        else:
            return False
        
    """Skip to the occurrence of string in file lines buffer"""
    def __SkipToToken(self, string):
        StartPos = self.__GetFileBufferPos(self)
        self.__SkipWhiteSpace(self)
        while not self.__EndOfFile(self):
            if self.__CurrentLine(self)[self.CurrentOffsetWithinLine , -1].find(string) == 0:
                self.CurrentOffsetWithinLine += len(string)
                return True
            self.__GetOneChar(self)
            self.__SkipWhiteSpace(self)

        self.__SetFileBufferPos(self, StartPos)
        return False

    """Return the tuple of current line and offset within the line"""
    def GetFileBufferPos(self):
        return (self.CurrentLineNumber, self.CurrentOffsetWithinLine)
    
    """Restore the file buffer position"""
    def SetFileBufferPos(self, pos):
        (self.CurrentLineNumber, self.CurrentOffsetWithinLine) = pos
            
    """Parse the file profile buffer to extract fd, fv ... information"""
    def ParseFile(self):
        while GetFd(self):
            pass
        else:
            return
        
        while GetFv(self):
            pass
        else:
            return
        
        while GetCapsule(self):
            pass
        else:
            return
        
        while GetVtf(self):
            pass
        else:
            return
        
        while GetRule(self):
            pass
        else:
            return

    def __GetFd(self):
        if not self.__IsToken(self, "[FD."):
            Warning("expected [FD.] At Line %d" % self.CurrentLineNumber)
            return False
        fdName = self.__GetFdUiName(self)
        Status = self.__GetCreateFile(self, fdName)
        if not Status:
            Warning("FD name error At Line %d" % self.CurrentLineNumber)
            return False
        
        if not self.__GetTokenStatements(self, fdName):
            return False
        
        self.__GetDefineStatements(self, fdName)
        if self.__ParserBreak:
            self.__ParserBreak = False
            Warning("DEFINE statement error At Line %d" % self.CurrentLineNumber)
            return False
            
        self.__GetSetStatements(self, fdName)
        if self.__ParserBreak:
            self.__ParserBreak = False
            Warning("SET statement error At Line %d" % self.CurrentLineNumber)
            return False
        
        if not self.__GetRegionLayout(self, fdName):
            Warning("expected region layout At Line %d" % self.CurrentLineNumber)
            return False
        while self.__GetRegionLayout(self, fdName):
            pass
        return True
    
    def __GetFdUiName(self):
        fdName = ""
        if self.__GetNextWord(self):
            fd = Fd.FD()
            fdName = fd.FdUiName = self.Token
            self.profile.FdDict[self.Token] = fd
        if not self.__IsToken(self, "]"):
            Warning("expected ']' At Line %d" % self.CurrentLineNumber)
            pass
        return fdName

    def __GetCreateFile(self, fdName):

        if self.__IsKeyword(self, "CREATE_FILE"):
            if not self.__IsToken(self, "="):
                Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                return False
            if not self.__GetNextWord(self):
                Warning("expected file name At Line %d" % self.CurrentLineNumber)
                return False
            fileName = self.Token
            if not self.__IsToken(self, ".fd"):
                Warning("expected '.fd' end At Line %d" % self.CurrentLineNumber)
                return False
            fileName += ".fd"
            fd = self.profile.FdDict[fdName]
            fd.CreateFileName = fileName

        return True

    def __GetTokenStatements(self, fdName):
        if not self.__IsKeyword(self, "BaseAddress"):
            Warning("BaseAddress missing At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__GetHexNumber(self):
            Warning("expected Hex base address At Line %d" % self.CurrentLineNumber)
            return False
        fd = self.profile.FdDict[fdName]
        fd.BaseAddress = self.Token
        
        if self.__IsToken(self, "|"):
            if self.__GetNextWord(self):
                fd.BaseAddressPcd = self.Token
            else:
                Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                return False

        if not self.__IsKeyword(self, "Size"):
            Warning("Size missing At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__GetHexNumber(self):
            Warning("expected Hex size At Line %d" % self.CurrentLineNumber)
            return False
      
        fd.Size = self.Token

        if self.__IsToken(self, "|"):
            if self.__GetNextWord(self):
                fd.SizePcd = self.Token
            else:
                Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                return False
        
        if not self.__IsKeyword(self, "ErasePolarity"):
            Warning("ErasePolarity missing At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__GetNextToken(self):
            Warning("expected Erase Polarity At Line %d" % self.CurrentLineNumber)
            return False
        if self.Token != "1" and self.Token != 0:
            Warning("expected 1 or 0 Erase Polarity At Line %d" % self.CurrentLineNumber)
            return False
        fd.ErasePolarity = self.Token

        Status = GetBlockStatements(self, fdName)
        return Status
    
    def __GetBlockStatements(self, fdName):
        
        if not GetBlockStatement(self, fdName):
            Warning("expected block statement At Line %d" % self.CurrentLineNumber)
            return False
        while GetBlockStatement(self, fdName):
            pass
        return True
    
    def __GetBlockStatement(self, fdName):
        if not self.__IsKeyword(self, "BlockSize"):
            Warning("Block size missing At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not self.__GetHexNumber(self):
            Warning("expected Hex block size At Line %d" % self.CurrentLineNumber)
            return False

        BlockSize = self.Token
        BlockSizePcd = None
        if self.__IsToken(self, "|"):
            if self.__GetNextWord(self):
                BlockSizePcd = self.Token
            else:
                Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                return False

        BlockNumber = "1"
        if self.__IsKeyword(self, "NumBlocks"):
            if not self.__IsToken(self, "="):
                Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                return False
            if not self.__GetDecimalNumber(self):
                Warning("expected block numbers At Line %d" % self.CurrentLineNumber)
                return False
            BlockNumber = self.Token
        
        fd = self.profile.FdDict[fdName]
        fd.BlockSizeList.append((BlockSize, BlockNumber, BlockSizePcd))
        return True

    def __GetDefineStatements(self, fdName):
        while GetDefineStatement(self, fdName):
            pass

    def __GetDefineStatement(self, fdName):
        if self.__IsKeyword("DEFINE"):
            self.__GetNextToken(self)
            macro = self.Token
            if not self.__IsToken(self, "="):
                self.__ParserBreak = True
                Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                return False
            if not self.__GetNextToken(self):
                self.__ParserBreak = True
                Warning("expected value At Line %d" % self.CurrentLineNumber)
                return False
            value = self.Token
            fd = self.profile.FdDict[fdName]
            fd.DefineVarDict[macro] = value
            return True
        
        return False

        
    def __GetSetStatements(self, fdName):
        while GetSetStatement(self, fdName):
            pass
        
    def __GetSetStatement(self, fdName):
        if self.__IsKeyword("SET"):
            if not self.__GetNextWord(self):
                self.__ParserBreak = True
                Warning("expected PCD CName At Line %d" % self.CurrentLineNumber)
                return False
            macro = self.Token
            if not self.__IsToken(self, "="):
                self.__ParserBreak = True
                Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                return False
            if not self.__GetNextToken(self):
                self.__ParserBreak = True
                Warning("expected value At Line %d" % self.CurrentLineNumber)
                return False
            value = self.Token
            fd = self.profile.FdDict[fdName]
            fd.SetVarDict[macro] = value
            return True

        return False

    def __GetRegionLayout(self, fdName):
        pass
        
    #CreateProfile()

    #GetCurrentLineNumber()
    
    """
    IsFdTag()
    IsFvTag()
    IsCapsuleTag()
    IsVtfTag()
    IsRulesTag()

    IsCName()
    IsSeperator()
    IsQuote()
    IsHexNumber()
    IsGuid()
    ...
    
    
    GetNextGuid()
    GetPcdCName()
    GetFileName()
    GetInfFile()
    GetInfOptions()
    ...
    
    GetBlockStatements()
    GetFvAttributes()
    GetAprioriSection()
    GetFileStatements()
    GetProcessFormat()
    GetComponentStatements()
    ...
    
    """
    
    
    
    
    
    