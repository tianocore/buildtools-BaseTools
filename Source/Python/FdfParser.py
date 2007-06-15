import Fd
import Region
import Fv
import AprioriSection

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

class Warning:
    def __init__(self, s):
        self.message = s

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
        
        self.FdDict = {}
        self.FvDict = {}
        
class FdfParser :
    

    def __init__(self, filename):
        self.profile = FileProfile(filename)
        self.CurrentLineNumber = 1
        self.CurrentOffsetWithinLine = 0
        self.__Token = ""
        self.__SkippedChars = ""

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
            while not self.__EndOfLine(self):
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

        StartPos = self.CurrentOffsetWithinLine
        while not self.__EndOfLine(self):
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
        self.__SkippedChars = str(self.__CurrentChar(self))
        while not self.__EndOfFile(self):
            if self.__CurrentLine(self)[self.CurrentOffsetWithinLine , -1].find(string) == 0:
                self.CurrentOffsetWithinLine += len(string)
                self.__SkippedChars += string
                return True
            self.__GetOneChar(self)
            self.__SkippedChars += str(self.__CurrentChar(self))
            self.__SkipWhiteSpace(self)

        self.__SetFileBufferPos(self, StartPos)
        self.__SkippedChars = ""
        return False

    """Return the tuple of current line and offset within the line"""
    def GetFileBufferPos(self):
        return (self.CurrentLineNumber, self.CurrentOffsetWithinLine)
    
    """Restore the file buffer position"""
    def SetFileBufferPos(self, pos):
        (self.CurrentLineNumber, self.CurrentOffsetWithinLine) = pos
            
    """Parse the file profile buffer to extract fd, fv ... information"""
    def ParseFile(self):

        try:
            while GetFd(self):
                pass

            while GetFv(self):
                pass

            while GetCapsule(self):
                pass

            while GetVtf(self):
                pass

            while GetRule(self):
                pass
            
        except Warning, X:
            print X.message + '\n'
            return
        
    def __GetFd(self):

        if not self.__GetNextToken(self):
            return False
        
        if self.__Token.startswith("[") and not self.__Token.startswith("[FD."):
            self.__UndoToken(self)
            return False
        
        if not self.__Token.startswith("[FD."):
            raise Warning("expected [FD.] At Line %d" % self.CurrentLineNumber)
        
        fdName = self.__GetFdUiName(self)
        fd = Fd.FD()
        fd.FdUiName = fdName
        self.profile.FdDict[fdName] = fd
        Status = self.__GetCreateFile(self, fd)
        if not Status:
            raise Warning("FD name error At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetTokenStatements(self, fd):
            return False
        
        self.__GetDefineStatements(self, fd)
##        if self.__ParserBreak:
##            self.__ParserBreak = False
##            Warning("DEFINE statement error At Line %d" % self.CurrentLineNumber)
##            return False
            
        self.__GetSetStatements(self, fd)
##        if self.__ParserBreak:
##            self.__ParserBreak = False
##            Warning("SET statement error At Line %d" % self.CurrentLineNumber)
##            return False
        
        if not self.__GetRegionLayout(self, fd):
            raise Warning("expected region layout At Line %d" % self.CurrentLineNumber)
            
        while self.__GetRegionLayout(self, fd):
            pass
        return True
    
    def __GetFdUiName(self):
        fdName = ""
        if self.__GetNextWord(self):
            fdName = self.__Token
        if not self.__IsToken(self, "]"):
            raise Warning("expected ']' At Line %d" % self.CurrentLineNumber)
            
        return fdName

    def __GetCreateFile(self, fd):

        if self.__IsKeyword(self, "CREATE_FILE"):
            if not self.__IsToken(self, "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetNextToken(self):
                raise Warning("expected file name At Line %d" % self.CurrentLineNumber)
                
            fileName = self.Token
##            if not self.__IsToken(self, ".fd"):
##                raise Warning("expected '.fd' end At Line %d" % self.CurrentLineNumber)
##
##            fileName += ".fd"
            fd.CreateFileName = fileName

        return True

    def __GetTokenStatements(self, fd):
        if not self.__IsKeyword(self, "BaseAddress"):
            raise Warning("BaseAddress missing At Line %d" % self.CurrentLineNumber)
           
        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetHexNumber(self):
            raise Warning("expected Hex base address At Line %d" % self.CurrentLineNumber)
            
        fd.BaseAddress = self.Token
        
        if self.__IsToken(self, "|"):
            if self.__GetNextWord(self):
                fd.BaseAddressPcd = self.Token
            else:
                raise Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)

        if not self.__IsKeyword(self, "Size"):
            raise Warning("Size missing At Line %d" % self.CurrentLineNumber)
            
        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetHexNumber(self):
            raise Warning("expected Hex size At Line %d" % self.CurrentLineNumber)
            
      
        fd.Size = self.Token

        if self.__IsToken(self, "|"):
            if self.__GetNextWord(self):
                fd.SizePcd = self.Token
            else:
                raise Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                
        
        if not self.__IsKeyword(self, "ErasePolarity"):
            raise Warning("ErasePolarity missing At Line %d" % self.CurrentLineNumber)
           
        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetNextToken(self):
            raise Warning("expected Erase Polarity At Line %d" % self.CurrentLineNumber)
            
        if self.Token != "1" and self.Token != 0:
            raise Warning("expected 1 or 0 Erase Polarity At Line %d" % self.CurrentLineNumber)
            
        fd.ErasePolarity = self.Token

        Status = GetBlockStatements(self, fd)
        return Status
    
    def __GetBlockStatements(self, fd):
        
        if not GetBlockStatement(self, fd):
            raise Warning("expected block statement At Line %d" % self.CurrentLineNumber)
            
        while GetBlockStatement(self, fd):
            pass
        return True
    
    def __GetBlockStatement(self, fd):
        if not self.__IsKeyword(self, "BlockSize"):
##            raise Warning("Block size missing At Line %d" % self.CurrentLineNumber)
            return False
        
        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetHexNumber(self):
            raise Warning("expected Hex block size At Line %d" % self.CurrentLineNumber)

        BlockSize = self.Token
        BlockSizePcd = None
        if self.__IsToken(self, "|"):
            if self.__GetNextWord(self):
                BlockSizePcd = self.Token
            else:
                raise Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)

        BlockNumber = "1"
        if self.__IsKeyword(self, "NumBlocks"):
            if not self.__IsToken(self, "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetDecimalNumber(self):
                raise Warning("expected block numbers At Line %d" % self.CurrentLineNumber)
                
            BlockNumber = self.Token
        
        fd.BlockSizeList.append((BlockSize, BlockNumber, BlockSizePcd))
        return True

    def __GetDefineStatements(self, obj):
        while GetDefineStatement(self, obj):
            pass
    
    def __GetDefineStatement(self, obj):
        if self.__IsKeyword("DEFINE"):
            self.__GetNextToken(self)
            macro = self.Token
            if not self.__IsToken(self, "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetNextToken(self):
                raise Warning("expected value At Line %d" % self.CurrentLineNumber)

            value = self.Token
            obj.DefineVarDict[macro] = value
            return True
        
        return False
    
    
    def __GetSetStatements(self, obj):
        while GetSetStatement(self, obj):
            pass

    def __GetSetStatement(self, obj):
        if self.__IsKeyword("SET"):
            if not self.__GetNextWord(self):
                raise Warning("expected PCD CName At Line %d" % self.CurrentLineNumber)
                
            macro = self.Token
            if not self.__IsToken(self, "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetNextToken(self):
                raise Warning("expected value At Line %d" % self.CurrentLineNumber)
                
            value = self.Token
            if value.startswith("{"):
                # deal with value with {}
                if not self.__SkipToToken(self, "}"):
                    raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
                value += self.__SkippedChars
                
            obj.SetVarDict[macro] = value
            return True

        return False

    def __GetRegionLayout(self, fd):
        if not self.__GetHexNumber(self):
            raise Warning("expected Region Offset At Line %d" % self.CurrentLineNumber)
        
        region = Region.region()
        region.Offset = self.__Token
        
        if not self.__IsToken(self, "|"):
            raise Warning("expected '|' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetHexNumber(self):
            raise Warning("expected Region Size At Line %d" % self.CurrentLineNumber)
        region.Size = self.__Token
        
        if not self.__GetNextWord(self):
            return False
        
        if not self.__Token in ("SET", "FV", "FILE", "DATA"):
            region.PcdOffset = self.__Token
            if not self.__IsToken(self, "|"):
                raise Warning("expected '|' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextWord(self):
                raise Warning("expected Region PCD Size At Line %d" % self.CurrentLineNumber)
            region.PcdSize = self.__Token
            
            if not self.__GetNextWord(self):
                return False

        if self.__Token == "SET":
            self.__GetSetStatements(self, region)
            if not self.__GetNextWord(self):
                return False
            
        if self.__Token == "FV":
            self.__UndoToken(self)
            self.__GetRegionFvType(self, region)
        elif self.__Token == "FILE":
            self.__UndoToken(self)
            self.__GetRegionFileType(self, region)
        else:
            self.__UndoToken(self)
            self.__GetRegionDataType(self, region)
            
        fd.RegionList.append(region)

        return True
            
    def __GetRegionFvType(self, region):

        if not self.__IsKeyword(self, "FV"):
            raise Warning("expected Keyword 'FV' At Line %d" % self.CurrentLineNumber)
        
        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetNextToken(self):
            raise Warning("expected FV name At Line %d" % self.CurrentLineNumber)
        
        region.RegionType = "FV"
        region.RegionData = self.__Token
        
    def __GetRegionFileType(self, region):

        if not self.__IsKeyword(self, "FILE"):
            raise Warning("expected Keyword 'FILE' At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextToken(self):
            raise Warning("expected File name At Line %d" % self.CurrentLineNumber)

        region.RegionType = "FILE"
        region.RegionData = self.__Token

    def __GetRegionDataType(self, region):
        
        if not self.__IsKeyword(self, "DATA"):
            raise Warning("expected Keyword 'DATA' At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__IsToken(self, "{"):
            raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetHexNumber(self):
            raise Warning("expected Hex byte At Line %d" % self.CurrentLineNumber)
        
        if len(self.__Token) > 4:
            raise Warning("Hex byte(must be 2 digits) too long At Line %d" % self.CurrentLineNumber)
        
        DataString = self.__Token
        DataString += ","
        
        while self.__GetHexNumber(self):
            if len(self.__Token) > 4:
                raise Warning("Hex byte(must be 2 digits) too long At Line %d" % self.CurrentLineNumber)
            DataString += self.__Token
            DataString += ","
            
        if not self.__IsToken(self, "}"):
            raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
        
        DataString = DataString.rstrip(",")
        region.RegionType = "DATA"
        region.RegionData = DataString
        
    def __GetFv(self):
        if not self.__GetNextToken(self):
            return False

        if self.__Token.startswith("[") and not self.__Token.startswith("[FV."):
            self.__UndoToken(self)
            return False

        if not self.__Token.startswith("[FV."):
            raise Warning("expected [FV.] At Line %d" % self.CurrentLineNumber)

        fvName = self.__GetFvUiName(self)
        fv = Fv.FV()
        fv.UiFvName = fvName
        self.profile.FvDict[fvName] = fv
        
        Status = self.__GetCreateFile(self, fv)
        if not Status:
            raise Warning("FV name error At Line %d" % self.CurrentLineNumber)

        self.__GetDefineStatements(self, fv)

        self.__GetBlockStatement(self, fv)

        self.__GetSetStatements(self, fv)

        self.__GetFvAlignment(self, fv)

        self.__GetAprioriSection(self, fv)
        
        while GetInfStatement(self, fv):
            pass

        while GetFileStatement(self, fv):
            pass
        
        return True


    def __GetFvAlignment(self, fv):
        
        if not self.__IsKeyword(self, "FvAlignment"):
            return False
        
        if not self.__IsToken(self, "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetNextWord(self):
            raise Warning("expected alignment value At Line %d" % self.CurrentLineNumber)
        
        fv.FvAlignment = self.__Token
        return True
    
    def __GetFvAttributes(self, fv):
        
        while self.__GetNextWord(self):
            name = self.__Token
            if name == "APRIORI":
                self.__UndoToken(self)
                return

            if not self.__IsToken(self, "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
            if not self.__GetNextToken(self) or self.__Token not in (TRUE, FALSE, 1, 0):
                raise Warning("expected TRUE/FALSE (1/0) At Line %d" % self.CurrentLineNumber)
            
            fv.FvAttributeDict[name] = self.__Token

        return

    def __GetAprioriSection(self, fv):
        
        if not self.__IsKeyword(self, "APRIORI"):
            return False
        
        if not self.__IsToken(self, "{"):
            raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)
        
        aprSection = AprioriSection.AprioriSection()
        while GetInfStatement(self, aprSection):
            pass
        
        while GetFileStatement(self, aprSection):
            pass
        
        if not self.__IsToken(self, "}"):
            raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)

        fv.AprioriSection = aprSection
        return True

    def __GetInfStatement(self, section):


    def __GetFileStatement(self, section):
        pass

    """
    GetNextGuid()

    ...
    
   GetProcessFormat()
    GetComponentStatements()
    ...
    
    """
    
    
    
    
    
    