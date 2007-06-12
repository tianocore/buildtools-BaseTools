import Fd

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

    """Whether char at current FileBufferPos is whitespace,"""
    def __IsWhiteSpace(self, char):
        if char in (T_CHAR_NULL, T_CHAR_CR, T_CHAR_SPACE, T_CHAR_TAB, T_CHAR_LF):
            return True
        else:
            return False

    """Skip white spaces from current char, return number of chars skipped"""
    def __SkipWhiteSpace(self):
        Count = 0
        while not EndOfFile(self):
            Count += 1
            CurrentLineLen = len(self.profile.FileLinesList[self.CurrentLineNumber-1])
            if CurrentChar(self) in (T_CHAR_NULL, T_CHAR_CR, T_CHAR_SPACE, T_CHAR_TAB):
                GetOneChar(self)
            if CurrentChar(self) == T_CHAR_LF:
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

        while not EndOfFile(self):
            
            # meet new line, then no longer in a comment for // and '#'
            if CurrentChar(self) == T_CHAR_LF:
                self.CurrentLineNumber += 1
                self.CurrentOffsetWithinLine = 0
                if InComment and DoubleSlashComment:
                    InComment = False
                    DoulbeSlashComment = False
                if InComment and HashComment:
                    InComment = False
                    HashComment = False
            # check for */ comment end
            elif InComment and not DoubleSlashComment and not HashComment and CurrentChar(self) == T_CHAR_STAR and NextChar(self) == T_CHAR_SLASH:
                SetCurrentCharValue(self, T_CHAR_SPACE)
                GetOneChar(self)
                SetCurrentCharValue(self, T_CHAR_SPACE)
                GetOneChar(self)
                InComment = False
            # set comments to spaces
            elif InComment:
                SetCurrentCharValue(self, T_CHAR_SPACE)
                GetOneChar(self)
            # check for // comment
            elif CurrentChar(self) == T_CHAR_SLASH and NextChar(self) == T_CHAR_SLASH and not EndOfLine(self):
                InComment = True
                DoubleSlashComment = True
            # check for '#' comment
            elif CurrentChar(self) == T_CHAR_HASH and not EndOfLine(self):
                InComment = True
                HashComment = True
            # check for /* comment start
            elif CurrentChar(self) == T_CHAR_SLASH and NextChar(self) == T_CHAR_STAR:
                SetCurrentCharValue(self, T_CHAR_SPACE)
                GetOneChar(self)
                SetCurrentCharValue(self, T_CHAR_SPACE)
                GetOneChar(self)
                InComment = True
            else:
                GetOneChar(self)

        # restore from ListOfList to ListOfString
        self.profile.FileLinesList = ["".join(list) for list in self.profile.FileLinesList]
        Rewind(self)

    """check whether input string is found from current char position along"""
    def __IsToken(self, string):
        SkipWhiteSpace(self)
        if EndOfFile(self):
            return False
        # Only consider the same line, no multi-line token allowed
        index = CurrentLine(self)[self.CurrentOffsetWithinLine, -1].find(string)
        if index == 0:
            self.CurrentOffsetWithinLine += len(string)
            return True
        return False

    """check whether input keyword is found from current char position along, whole word only!"""
    def __IsKeyword(self, keyword):
        SkipWhiteSpace(self)
        if EndOfFile(self):
            return False
        # Only consider the same line, no multi-line token allowed
        index = CurrentLine(self)[self.CurrentOffsetWithinLine, -1].find(keyword)
        if index == 0:
            if not str(CurrentLine(self)[self.CurrentOffsetWithinLine + len(keyword)]).isspace() and \
            CurrentLine(self)[self.CurrentOffsetWithinLine + len(keyword)] != '=':
                return False
            self.CurrentOffsetWithinLine += len(keyword)
            return True
        return False

    """get next C name from file lines"""
    def __GetNextWord(self):
        SkipWhiteSpace(self)
        if EndOfFile(self):
            return False
        
        TempChar = CurrentChar(self)
        StartPos = self.CurrentOffsetWithinLine
        if (TempChar >= 'a' and TempChar <= 'z') or (TempChar >= 'A' and TempChar <= 'Z') or TempChar == '_':
            GetOneChar(self)
            while not EndOfFile(self):
                TempChar = CurrentChar(self)
                if (TempChar >= 'a' and TempChar <= 'z') or (TempChar >= 'A' and TempChar <= 'Z') \
                or (TempChar >= '0' and TempChar <= '9') or TempChar == '_' or TempChar == '-':
                    GetOneChar(self)
                    
                else:
                    break

            self.Token = CurrentLine[StartPos, self.CurrentOffsetWithinLine]
            return True
        #elif ...:
            # other conditions
        #    return True
            
        return False
    
    def __GetNextToken(self):
        SkipWhiteSpace(self)
        if EndOfFile(self):
            return False

        while not EndOfFile(self):
                TempChar = CurrentChar(self)
                if not str(TempChar).isspace():
                    GetOneChar(self)
                else:
                    break
        else:
            return False
        
        self.Token = CurrentLine[StartPos, self.CurrentOffsetWithinLine]
        return True

    def __UndoToken(self):
        while UndoOneChar(self) and not str(CurrentChar(self)).isspace():
            pass
    
    def __HexDigit(self, TempChar):
        if (TempChar >= 'a' and TempChar <= 'f') or (TempChar >= 'A' and TempChar <= 'F') \
                or (TempChar >= '0' and TempChar <= '9'):
                    return True
        else:
            return False
        
    def __GetHexNumber(self):
        if not GetNextToken(self):
            return False
        if not self.Token.startswith("0x"):
            return False
        if len(self.Token) <= 2:
            return False
        charList = [c for c in self.Token[2, -1] if not HexDigit(self, c)]
        if len(charList) == 0:
            return True
        else:
            return False
        
    def __GetDecimalNumber(self):
        if not GetNextToken(self):
            return False
        if self.Token.isdigit():
            return True
        else:
            return False
        
    """Skip to the occurrence of string in file lines buffer"""
    def __SkipToToken(self, string):
        StartPos = GetFileBufferPos(self)
        SkipWhiteSpace(self)
        while not EndOfFile(self):
            if CurrentLine(self)[self.CurrentOffsetWithinLine , -1].find(string) == 0:
                self.CurrentOffsetWithinLine += len(string)
                return True
            GetOneChar(self)
            SkipWhiteSpace(self)

        SetFileBufferPos(self, StartPos)
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
        if not IsToken(self, "[FD."):
            Warning("expected [FD.] At Line %d" % self.CurrentLineNumber)
            return False
        fdName = GetFdUiName(self)
        Status = GetCreateFile(self, fdName)
        if not Status:
            Warning("FD name error At Line %d" % self.CurrentLineNumber)
            return False
        
        if not GetTokenStatements(self, fdName):
            return False
        
        Status = GetDefineStatements(self, fdName)
        if not Status:
            Warning("DEFINE statement error At Line %d" % self.CurrentLineNumber)
            return False
            
        Status = GetSetStatements(self, fdName)
        if not Status:
            Warning("SET statement error At Line %d" % self.CurrentLineNumber)
            return False
        
        if not GetRegionLayout(self, fdName):
            Warning("expected region layout At Line %d" % self.CurrentLineNumber)
            return False
        while GetRegionLayout(self, fdName):
            pass
        return True
    
    def __GetFdUiName(self):
        fdName = ""
        if GetNextWord(self):
            fd = Fd.FD()
            fdName = fd.FdUiName = self.Token
            self.profile.FdDict[self.Token] = fd
        if not IsToken(self, "]"):
            Warning("expected ']' At Line %d" % self.CurrentLineNumber)
            pass
        return fdName

    def __GetCreateFile(self, fdName):

        if IsKeyWord(self, "CREATE_FILE"):
            if not IsToken(self, "="):
                Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                return False
            if not GetNextWord(self):
                Warning("expected file name At Line %d" % self.CurrentLineNumber)
                return False
            fileName = self.Token
            if not IsToken(self, ".fd"):
                Warning("expected '.fd' end At Line %d" % self.CurrentLineNumber)
                return False
            fileName += ".fd"
            fd = self.profile.FdDict[fdName]
            fd.CreateFileName = fileName

        return True

    def __GetTokenStatements(self, fdName):
        if not IsKeyword(self, "BaseAddress"):
            Warning("BaseAddress missing At Line %d" % self.CurrentLineNumber)
            return False
        if not IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not GetHexNumber(self):
            Warning("expected Hex base address At Line %d" % self.CurrentLineNumber)
            return False
        fd = self.profile.FdDict[fdName]
        fd.BaseAddress = self.Token
        
        if IsToken(self, "|"):
            if GetNextWord(self):
                fd.BaseAddressPcd = self.Token
            else:
                Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                return False

        if not IsKeyword(self, "Size"):
            Warning("Size missing At Line %d" % self.CurrentLineNumber)
            return False
        if not IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not GetHexNumber(self):
            Warning("expected Hex size At Line %d" % self.CurrentLineNumber)
            return False
      
        fd.Size = self.Token

        if IsToken(self, "|"):
            if GetNextWord(self):
                fd.SizePcd = self.Token
            else:
                Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                return False
        
        if not IsKeyword(self, "ErasePolarity"):
            Warning("ErasePolarity missing At Line %d" % self.CurrentLineNumber)
            return False
        if not IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not GetNextToken(self):
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
        if not IsKeyword(self, "BlockSize"):
            Warning("Block size missing At Line %d" % self.CurrentLineNumber)
            return False
        if not IsToken(self, "="):
            Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            return False
        if not GetHexNumber(self):
            Warning("expected Hex block size At Line %d" % self.CurrentLineNumber)
            return False

        BlockSize = self.Token
        BlockSizePcd = None
        if IsToken(self, "|"):
            if GetNextWord(self):
                BlockSizePcd = self.Token
            else:
                Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                return False

        BlockNumber = "1"
        if IsKeyword(self, "NumBlocks"):
            if not IsToken(self, "="):
                Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                return False
            if not GetDecimalNumber(self):
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
        if IsKeyword("DEFINE"):
            GetNextToken(self)
            macro = self.Token
            if not IsToken(self, "="):
                Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        
    def __GetSetStatements(self, fdName):
        while GetSetStatement(self, fdName):
            pass
        
    def __GetRegionLayout(self, fdName):
        
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
    
    
    
    
    
    