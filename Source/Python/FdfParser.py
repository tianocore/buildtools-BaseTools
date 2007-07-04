import Fd
import Region
import Fv
import AprioriSection
import FfsInfStatement
import FfsFileStatement
import VerSection
import UiSection
import FvImageSection
import DataSection
import CompressSection
import GuidSection
import Capsule
import CapsuleData
import Rule
import RuleComplexFile
import RuleSimpleFile
import EfiSection
import Vtf
import ComponentStatement

import re

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
                self.FileLinesList = [list(s) for s in self.FileLinesList]
            finally:
                fsock.close()

        except IOError:
            print "Error when opening file."
            return
        
        self.FdDict = {}
        self.FvDict = {}
        self.CapsuleList = []
#        self.RuleList = []
        self.VtfList = []
        self.RuleDict = {}
        
class FdfParser:
    

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
        while not self.__EndOfFile():
            Count += 1
            if self.__CurrentChar() in (T_CHAR_NULL, T_CHAR_CR, T_CHAR_LF, T_CHAR_SPACE, T_CHAR_TAB):
                self.__SkippedChars += str(self.__CurrentChar())
                self.__GetOneChar()
##            elif self.__CurrentChar() == T_CHAR_LF:
##                self.CurrentLineNumber += 1
##                self.CurrentOffsetWithinLine = 0
            else:
                return Count - 1

    """Judge current buffer pos is at file end"""
    def __EndOfFile(self):
        NumberOfLines = len(self.profile.FileLinesList)
        SizeOfLastLine = len(self.profile.FileLinesList[-1])
        if self.CurrentLineNumber == NumberOfLines and self.CurrentOffsetWithinLine >= SizeOfLastLine - 1:
            return True
        else:
            return False

    """Judge current char is at line end"""
    def __EndOfLine(self):
        SizeOfCurrentLine = len(self.profile.FileLinesList[self.CurrentLineNumber - 1])
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
            self.CurrentOffsetWithinLine = len(self.__CurrentLine()) - 1
        else:
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
    ### BUGBUG: No !include statement processing contained in this procedure
    ### !include statement should be expanded at the same FileLinesList[CurrentLineNumber - 1]
    def PreprocessFile(self):
        # change string to list of chars, as string can NOT be modified
        

        self.Rewind()
        InComment = False
        DoubleSlashComment = False
        HashComment = False

        while not self.__EndOfFile():
            
            # meet new line, then no longer in a comment for // and '#'
            if self.__CurrentChar() == T_CHAR_LF:
                self.CurrentLineNumber += 1
                self.CurrentOffsetWithinLine = 0
                if InComment and DoubleSlashComment:
                    InComment = False
                    DoubleSlashComment = False
                if InComment and HashComment:
                    InComment = False
                    HashComment = False
            # check for */ comment end
            elif InComment and not DoubleSlashComment and not HashComment and self.__CurrentChar() == T_CHAR_STAR and self.__NextChar() == T_CHAR_SLASH:
                self.__SetCurrentCharValue(T_CHAR_SPACE)
                self.__GetOneChar()
                self.__SetCurrentCharValue(T_CHAR_SPACE)
                self.__GetOneChar()
                InComment = False
            # set comments to spaces
            elif InComment:
                self.__SetCurrentCharValue(T_CHAR_SPACE)
                self.__GetOneChar()
            # check for // comment
            elif self.__CurrentChar() == T_CHAR_SLASH and self.__NextChar() == T_CHAR_SLASH and not self.__EndOfLine():
                InComment = True
                DoubleSlashComment = True
            # check for '#' comment
            elif self.__CurrentChar() == T_CHAR_HASH and not self.__EndOfLine():
                InComment = True
                HashComment = True
            # check for /* comment start
            elif self.__CurrentChar() == T_CHAR_SLASH and self.__NextChar() == T_CHAR_STAR:
                self.__SetCurrentCharValue( T_CHAR_SPACE)
                self.__GetOneChar()
                self.__SetCurrentCharValue( T_CHAR_SPACE)
                self.__GetOneChar()
                InComment = True
            else:
                self.__GetOneChar()

        # restore from ListOfList to ListOfString
        self.profile.FileLinesList = ["".join(list) for list in self.profile.FileLinesList]
        self.Rewind()

    """check whether input string is found from current char position along"""
    def __IsToken(self, string, ignoreCase = False):
        self.__SkipWhiteSpace()
##        if self.__EndOfFile():
##            return False
        # Only consider the same line, no multi-line token allowed
        StartPos = self.CurrentOffsetWithinLine
        index = -1
        if ignoreCase:
            index = self.__CurrentLine()[self.CurrentOffsetWithinLine : ].upper().find(string.upper()) 
        else:
            index = self.__CurrentLine()[self.CurrentOffsetWithinLine : ].find(string)
        if index == 0:
            self.CurrentOffsetWithinLine += len(string)
            self.__Token = self.__CurrentLine()[StartPos : self.CurrentOffsetWithinLine]
            return True
        return False

    """check whether input keyword is found from current char position along, whole word only!"""
    def __IsKeyword(self, keyword, ignoreCase = False):
        self.__SkipWhiteSpace()
##        if self.__EndOfFile():
##            return False
        # Only consider the same line, no multi-line token allowed
        StartPos = self.CurrentOffsetWithinLine
        index = -1
        if ignoreCase:
            index = self.__CurrentLine()[self.CurrentOffsetWithinLine : ].upper().find(keyword.upper()) 
        else:
            index = self.__CurrentLine()[self.CurrentOffsetWithinLine : ].find(keyword)
        if index == 0:
            followingChar = self.__CurrentLine()[self.CurrentOffsetWithinLine + len(keyword)]
            if not str(followingChar).isspace() and followingChar not in ('=', '|'):
                return False
            self.CurrentOffsetWithinLine += len(keyword)
            self.__Token = self.__CurrentLine()[StartPos : self.CurrentOffsetWithinLine]
            return True
        return False

    """get next C name from file lines"""
    def __GetNextWord(self):
        self.__SkipWhiteSpace()
        if self.__EndOfFile():
            return False
        
        TempChar = self.__CurrentChar()
        StartPos = self.CurrentOffsetWithinLine
        if (TempChar >= 'a' and TempChar <= 'z') or (TempChar >= 'A' and TempChar <= 'Z') or TempChar == '_':
            self.__GetOneChar()
            while not self.__EndOfLine():
                TempChar = self.__CurrentChar()
                if (TempChar >= 'a' and TempChar <= 'z') or (TempChar >= 'A' and TempChar <= 'Z') \
                or (TempChar >= '0' and TempChar <= '9') or TempChar == '_' or TempChar == '-':
                    self.__GetOneChar()
                    
                else:
                    break

            self.__Token = self.__CurrentLine()[StartPos : self.CurrentOffsetWithinLine]
            return True
        #elif ...:
            # other conditions
        #    return True
            
        return False
    
    def __GetNextToken(self):
        self.__SkipWhiteSpace()
        if self.__EndOfFile():
            return False

        StartPos = self.CurrentOffsetWithinLine
        while not self.__EndOfLine():
                TempChar = self.__CurrentChar()
                if not str(TempChar).isspace() and TempChar not in ('=', '|', ',', '}'):
                    self.__GetOneChar()
                else:
                    break
        else:
            return False
        
        if StartPos != self.CurrentOffsetWithinLine:
            self.__Token = self.__CurrentLine()[StartPos : self.CurrentOffsetWithinLine]
            return True
        else:
            return False

    def __GetNextGuid(self):
        
        if not self.__GetNextToken():
            return False
        p = re.compile('[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}')
        if p.match(self.__Token) != None:
            return True
        else:
            self.__UndoToken()
            return False

    def __UndoToken(self):
        self.__UndoOneChar()
        while self.__CurrentChar().isspace():
            self.__UndoOneChar()
        while not str(self.__CurrentChar()).isspace() and self.__CurrentChar() not in ('=', '|', ','):
            self.__UndoOneChar()
        self.__GetOneChar()
    
    def __HexDigit(self, TempChar):
        if (TempChar >= 'a' and TempChar <= 'f') or (TempChar >= 'A' and TempChar <= 'F') \
                or (TempChar >= '0' and TempChar <= '9'):
                    return True
        else:
            return False
        
    def __GetHexNumber(self):
        if not self.__GetNextToken():
            return False
        if not self.__Token.upper().startswith("0X"):
            self.__UndoToken()
            return False
        if len(self.__Token) <= 2:
            self.__UndoToken()
            return False
        charList = [c for c in self.__Token[2 : ] if not self.__HexDigit( c)]
        if len(charList) == 0:
            return True
        else:
            self.__UndoToken()
            return False
        
    def __GetDecimalNumber(self):
        if not self.__GetNextToken():
            return False
        if self.__Token.isdigit():
            return True
        else:
            self.__UndoToken()
            return False
        
    """Skip to the occurrence of string in file lines buffer"""
    def __SkipToToken(self, string, ignoreCase = False):
        StartPos = self.GetFileBufferPos()
        self.__SkipWhiteSpace()
        self.__SkippedChars = ""
        while not self.__EndOfFile():
            index = -1
            if ignoreCase:
                index = self.__CurrentLine()[self.CurrentOffsetWithinLine : ].upper().find(string.upper()) 
            else:
                index = self.__CurrentLine()[self.CurrentOffsetWithinLine : ].find(string)
            if index == 0:
                self.CurrentOffsetWithinLine += len(string)
                self.__SkippedChars += string
                return True
            self.__SkippedChars += str(self.__CurrentChar())
            self.__GetOneChar()
            self.__SkipWhiteSpace()

        self.SetFileBufferPos( StartPos)
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
            self.PreprocessFile()
            while self.__GetFd():
                pass

            while self.__GetFv():
                pass

            while self.__GetCapsule():
                pass

            while self.__GetVtf():
                pass

            while self.__GetRule():
                pass
            
        except Warning, X:
            self.__UndoToken()
            print 'Got Token: %s' % self.__Token
            print 'Parsing String: %s At line: %d, Offset Within Line: %d' \
                    % (self.profile.FileLinesList[self.CurrentLineNumber - 1][self.CurrentOffsetWithinLine :], self.CurrentLineNumber, self.CurrentOffsetWithinLine)
            print X.message
            raise
        
    def __GetFd(self):

        if not self.__GetNextToken():
            return False
        
        S = self.__Token.upper()
        if S.startswith("[") and not S.startswith("[FD."):
            if not S.startswith("[FV.") and not S.startswith("[CAPSULE.") \
                and not S.startswith("[VTF.") and not S.startswith("[RULE."):
                raise Warning("Unknown section At Line %d" % self.CurrentLineNumber)
            self.__UndoToken()
            return False
        
        self.__UndoToken()
        if not self.__IsToken("[FD.", True):
            raise Warning("expected [FD.] At Line %d" % self.CurrentLineNumber)
        
        fdName = self.__GetUiName()
        
        if not self.__IsToken( "]"):
            raise Warning("expected ']' At Line %d" % self.CurrentLineNumber)
        
        fd = Fd.FD()
        fd.FdUiName = fdName.upper()
        self.profile.FdDict[fdName.upper()] = fd
        Status = self.__GetCreateFile( fd)
        if not Status:
            raise Warning("FD name error At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetTokenStatements( fd):
            return False
        
        self.__GetDefineStatements( fd)

        self.__GetSetStatements( fd)

        if not self.__GetRegionLayout( fd):
            raise Warning("expected region layout At Line %d" % self.CurrentLineNumber)
            
        while self.__GetRegionLayout( fd):
            pass
        return True
    
    def __GetUiName(self):
        fdName = ""
        if self.__GetNextWord():
            fdName = self.__Token
            
        return fdName

    def __GetCreateFile(self, fd):

        if self.__IsKeyword( "CREATE_FILE"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetNextToken():
                raise Warning("expected file name At Line %d" % self.CurrentLineNumber)
                
            fileName = self.__Token
##            if not self.__IsToken( ".fd"):
##                raise Warning("expected '.fd' end At Line %d" % self.CurrentLineNumber)
##
##            fileName += ".fd"
            fd.CreateFileName = fileName

        return True

    def __GetTokenStatements(self, fd):
        if not self.__IsKeyword( "BaseAddress"):
            raise Warning("BaseAddress missing At Line %d" % self.CurrentLineNumber)
           
        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetHexNumber():
            raise Warning("expected Hex base address At Line %d" % self.CurrentLineNumber)
            
        fd.BaseAddress = self.__Token
        
        if self.__IsToken( "|"):
            if self.__GetNextWord():
                fd.BaseAddressPcd = self.__Token
            else:
                raise Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)

        if not self.__IsKeyword( "Size"):
            raise Warning("Size missing At Line %d" % self.CurrentLineNumber)
            
        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetHexNumber():
            raise Warning("expected Hex size At Line %d" % self.CurrentLineNumber)
            
      
        fd.Size = long(self.__Token, 0)

        if self.__IsToken( "|"):
            if self.__GetNextWord():
                fd.SizePcd = self.__Token
            else:
                raise Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)
                
        
        if not self.__IsKeyword( "ErasePolarity"):
            raise Warning("ErasePolarity missing At Line %d" % self.CurrentLineNumber)
           
        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetNextToken():
            raise Warning("expected Erase Polarity At Line %d" % self.CurrentLineNumber)
            
        if self.__Token != "1" and self.__Token != "0":
            raise Warning("expected 1 or 0 Erase Polarity At Line %d" % self.CurrentLineNumber)
            
        fd.ErasePolarity = self.__Token

        Status = self.__GetBlockStatements(fd)
        return Status
    
    def __GetBlockStatements(self, obj):
        
        if not self.__GetBlockStatement(obj):
            raise Warning("expected block statement At Line %d" % self.CurrentLineNumber)
            
        while self.__GetBlockStatement(obj):
            pass
        return True
    
    def __GetBlockStatement(self, obj):
        if not self.__IsKeyword( "BlockSize"):
##            raise Warning("Block size missing At Line %d" % self.CurrentLineNumber)
            return False
        
        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
        if not self.__GetHexNumber() and not self.__GetDecimalNumber():
            raise Warning("expected Hex block size At Line %d" % self.CurrentLineNumber)

        BlockSize = long(self.__Token, 0)
        BlockSizePcd = None
        if self.__IsToken( "|"):
            if self.__GetNextWord():
                BlockSizePcd = self.__Token
            else:
                raise Warning("expected PcdCName At Line %d" % self.CurrentLineNumber)

        BlockNumber = 0x1
        if self.__IsKeyword( "NumBlocks"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetDecimalNumber() and not self.__GetHexNumber():
                raise Warning("expected block numbers At Line %d" % self.CurrentLineNumber)
                
            BlockNumber = long(self.__Token, 0)
        
        obj.BlockSizeList.append((BlockSize, BlockNumber, BlockSizePcd))
        return True

    def __GetDefineStatements(self, obj):
        while self.__GetDefineStatement( obj):
            pass
    
    def __GetDefineStatement(self, obj):
        if self.__IsKeyword("DEFINE"):
            self.__GetNextToken()
            macro = self.__Token
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetNextToken():
                raise Warning("expected value At Line %d" % self.CurrentLineNumber)

            value = self.__Token
            obj.DefineVarDict[macro] = value
            return True
        
        return False
    
    
    def __GetSetStatements(self, obj):
        while self.__GetSetStatement(obj):
            pass

    def __GetSetStatement(self, obj):
        if self.__IsKeyword("SET"):
            if not self.__GetNextWord():
                raise Warning("expected PCD CName At Line %d" % self.CurrentLineNumber)
                
            macro = self.__Token
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                
            if not self.__GetNextToken():
                raise Warning("expected value At Line %d" % self.CurrentLineNumber)
                
            value = self.__Token
            if value.startswith("{"):
                # deal with value with {}
                if not self.__SkipToToken( "}"):
                    raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
                value += self.__SkippedChars
                
            obj.SetVarDict[macro] = value
            return True

        return False

    def __GetRegionLayout(self, fd):
        if not self.__GetHexNumber():
##            raise Warning("expected Region Offset At Line %d" % self.CurrentLineNumber)
            return False
        
        region = Region.region()
        region.Offset = long(self.__Token, 0)
        fd.RegionList.append(region)
        
        if not self.__IsToken( "|"):
            raise Warning("expected '|' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetHexNumber():
            raise Warning("expected Region Size At Line %d" % self.CurrentLineNumber)
        region.Size = long(self.__Token, 0)
        
        if not self.__GetNextWord():
            return True
        
        if not self.__Token in ("SET", "FV", "FILE", "DATA"):
            region.PcdOffset = self.__Token
            if not self.__IsToken( "|"):
                raise Warning("expected '|' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextWord():
                raise Warning("expected Region PCD Size At Line %d" % self.CurrentLineNumber)
            region.PcdSize = self.__Token
            
            if not self.__GetNextWord():
                return True

        if self.__Token == "SET":
            self.__UndoToken()
            self.__GetSetStatements( region)
            if not self.__GetNextWord():
                return True
            
        if self.__Token == "FV":
            self.__UndoToken()
            self.__GetRegionFvType( region)

        elif self.__Token == "FILE":
            self.__UndoToken()
            self.__GetRegionFileType( region)

        else:
            self.__UndoToken()
            self.__GetRegionDataType( region)
            
        return True
            
    def __GetRegionFvType(self, region):

        if not self.__IsKeyword( "FV"):
            raise Warning("expected Keyword 'FV' At Line %d" % self.CurrentLineNumber)
        
        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetNextToken():
            raise Warning("expected FV name At Line %d" % self.CurrentLineNumber)
        
        region.RegionType = "FV"
        region.RegionData = self.__Token
        
    def __GetRegionFileType(self, region):

        if not self.__IsKeyword( "FILE"):
            raise Warning("expected Keyword 'FILE' At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextToken():
            raise Warning("expected File name At Line %d" % self.CurrentLineNumber)

        region.RegionType = "FILE"
        region.RegionData = self.__Token

    def __GetRegionDataType(self, region):
        
        if not self.__IsKeyword( "DATA"):
            raise Warning("expected Region Data type At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__IsToken( "{"):
            raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetHexNumber():
            raise Warning("expected Hex byte At Line %d" % self.CurrentLineNumber)
        
        if len(self.__Token) > 4:
            raise Warning("Hex byte(must be 2 digits) too long At Line %d" % self.CurrentLineNumber)
        
        DataString = self.__Token
        DataString += ","
        
        while self.__IsToken(","):
            self.__GetHexNumber()
            if len(self.__Token) > 4:
                raise Warning("Hex byte(must be 2 digits) too long At Line %d" % self.CurrentLineNumber)
            DataString += self.__Token
            DataString += ","
            
        if not self.__IsToken( "}"):
            raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
        
        DataString = DataString.rstrip(",")
        region.RegionType = "DATA"
        region.RegionData = DataString
        
    def __GetFv(self):
        if not self.__GetNextToken():
            return False

        S = self.__Token.upper()
        if S.startswith("[") and not S.startswith("[FV."):
            if not S.startswith("[CAPSULE.") \
                and not S.startswith("[VTF.") and not S.startswith("[RULE."):
                raise Warning("Unknown section or section appear sequence error At Line %d.\n \
                            The correct sequence should be [FD.], [FV.], [Capsule.], [VTF.], [Rule.]" % self.CurrentLineNumber)
            self.__UndoToken()
            return False

        self.__UndoToken()
        if not self.__IsToken("[FV.", True):
##            raise Warning("expected [FV.] At Line %d" % self.CurrentLineNumber)
            raise Warning("Unknown Keyword At Line %d" % self.CurrentLineNumber)
        
        fvName = self.__GetUiName()
        if not self.__IsToken( "]"):
            raise Warning("expected ']' At Line %d" % self.CurrentLineNumber)
        
        fv = Fv.FV()
        fv.UiFvName = fvName.upper()
        self.profile.FvDict[fvName.upper()] = fv
        
        Status = self.__GetCreateFile( fv)
        if not Status:
            raise Warning("FV name error At Line %d" % self.CurrentLineNumber)

        self.__GetDefineStatements( fv)

        self.__GetBlockStatement( fv)

        self.__GetSetStatements( fv)

        self.__GetFvAlignment( fv)

        self.__GetFvAttributes( fv)
        
        self.__GetAprioriSection( fv)
        
        while True:
            isInf = self.__GetInfStatement( fv)
            isFile = self.__GetFileStatement( fv)
            if not isInf and not isFile:
                break
        
        return True


    def __GetFvAlignment(self, fv):
        
        if not self.__IsKeyword( "FvAlignment"):
            return False
        
        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetNextToken():
            raise Warning("expected alignment value At Line %d" % self.CurrentLineNumber)
        
        if self.__Token.upper() not in ("1", "2", "4", "8", "16", "32", "64", "128", "256", "512", \
                                        "1K", "2K", "4K", "8K", "16K", "32K", "64K", "128K", "256K", "512K", \
                                        "1M", "2M", "4M", "8M", "16M", "32M", "64M", "128M", "256M", "512M", \
                                        "1G", "2G"):
            raise Warning("Unknown alignment value At Line %d" % self.CurrentLineNumber)
        fv.FvAlignment = self.__Token
        return True
    
    def __GetFvAttributes(self, fv):
        
        while self.__GetNextWord():
            name = self.__Token
            if name not in ("ERASE_POLARITY", "MEMORY_MAPPED", \
                           "STICKY_WRITE", "LOCK_CAP", "LOCK_STATUS", "WRITE_ENABLED_CAP", \
                           "WRITE_DISABLED_CAP", "WRITE_STATUS", "READ_ENABLED_CAP", \
                           "READ_DISABLED_CAP", "READ_STATUS", "READ_LOCK_CAP", \
                           "READ_LOCK_STATUS", "WRITE_LOCK_CAP", "WRITE_LOCK_STATUS", \
                           "WRITE_POLICY_RELIABLE"):
                self.__UndoToken()
                return

            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
            if not self.__GetNextToken() or self.__Token.upper() not in ("TRUE", "FALSE", "1", "0"):
                raise Warning("expected TRUE/FALSE (1/0) At Line %d" % self.CurrentLineNumber)
            
            fv.FvAttributeDict[name] = self.__Token

        return

    def __GetAprioriSection(self, fv):
        
        if not self.__IsKeyword( "APRIORI"):
            return False
        
        if not self.__IsToken( "{"):
            raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)
        
        aprSection = AprioriSection.AprioriSection()
        self.__GetDefineStatements(aprSection)
        while self.__GetInfStatement( aprSection):
            pass
        
        while self.__GetFileStatement( aprSection):
            pass
        
        if not self.__IsToken( "}"):
            raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)

        fv.AprioriSection = aprSection
        return True

    def __GetInfStatement(self, obj):

        if not self.__IsKeyword( "INF"):
            return False
        
        ffsInf = FfsInfStatement.FfsInfStatement()
        self.__GetInfOptions( ffsInf)
        
        if not self.__GetNextToken():
            raise Warning("expected INF file path At Line %d" % self.CurrentLineNumber)
        ffsInf.InfFileName = self.__Token
        
        obj.FfsList.append(ffsInf)
        return True
    
    def __GetInfOptions(self, ffsInf):
        
        if self.__IsKeyword( "RuleOverride"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextToken():
                raise Warning("expected Rule name At Line %d" % self.CurrentLineNumber)
            ffsInf.Rule = self.__Token
            
        if self.__IsKeyword( "VERSION"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextToken():
                raise Warning("expected Version At Line %d" % self.CurrentLineNumber)
            ffsInf.ver = self.__Token
        
        if self.__IsKeyword( "UI"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextToken():
                raise Warning("expected UI name At Line %d" % self.CurrentLineNumber)
            ffsInf.Ui = self.__Token

        if self.__GetNextWord():
            p = re.compile(r'(([a-fA-F0-9]+)|\*)_(([a-fA-F0-9]+)|\*)_(([a-fA-F0-9]+)|\*)')
            if p.match(self.__Token):
                ffsInf.KeyStringList.append(self.__Token)
                if not self.__IsToken(","):
                    return
            else:
                self.__UndoToken()
                return
                
            while self.__GetNextWord:
                if not p.match(self.__Token):
                    raise Warning("expected KeyString \"Target_Tag_Arch\" At Line %d" % self.CurrentLineNumber)
                ffsInf.KeyStringList.append(self.__Token)

                if not self.__IsToken(","):
                    break
                


    def __GetFileStatement(self, obj):

        if not self.__IsKeyword( "FILE"):
            return False
        
        ffsFile = FfsFileStatement.FileStatements()
        
        if not self.__GetNextWord():
            raise Warning("expected FFS type At Line %d" % self.CurrentLineNumber)
        ffsFile.FvType = self.__Token
        
        if not self.__IsToken( "="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextGuid():
            raise Warning("expected File GUID At Line %d" % self.CurrentLineNumber)
        ffsFile.NameGuid = self.__Token
    
        self.__GetFilePart( ffsFile)
        obj.FfsList.append(ffsFile)
        return True
        
    def __GetFilePart(self, ffsFile):
        
        self.__GetFileOpts( ffsFile)
        
        if not self.__GetNextToken():
            raise Warning("expected File name or section data At Line %d" % self.CurrentLineNumber)
        
        if self.__Token == "{":
            self.__UndoToken()
            self.__GetSectionData( ffsFile)
        else:
            ffsFile.FilePath = self.__Token
        
    
    def __GetFileOpts(self, ffsFile):

        if self.__IsKeyword( "FIXED", True):
            ffsFile.Fixed = True
            
        if self.__IsKeyword( "CHECKSUM", True):
            ffsFile.CheckSum = True
            
        if self.__GetAlignment():
            ffsFile.Alignment = self.__Token
    
    def __GetAlignment(self):
        if self.__IsKeyword( "Align", True):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
            if not self.__GetNextToken():
                raise Warning("expected alignment value At Line %d" % self.CurrentLineNumber)
            
        return False
    
    def __GetSectionData(self, ffsFile):
        
        if self.__IsToken( "{"):
            while True:
                isLeafSection = self.__GetLeafSection(ffsFile)
                isEncapSection = self.__GetEncapsulationSec(ffsFile)
                if not isLeafSection and not isEncapSection:
                    break

            if not self.__IsToken( "}"):
                raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
    
    def __GetLeafSection(self, obj):
        
        oldPos = self.GetFileBufferPos()
        
        if not self.__IsKeyword( "SECTION"):
            if len(obj.SectionList) == 0:
                raise Warning("expected SECTION At Line %d" % self.CurrentLineNumber)
            else:
                return False
        
        alignment = None
        if self.__GetAlignment():
            alignment = self.__Token
            
        buildNum = None
        if self.__IsKeyword( "BUILD_NUM"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
            if not self.__GetNextToken():
                raise Warning("expected Build number value At Line %d" % self.CurrentLineNumber)
            
            buildNum = self.__Token
            
        if self.__IsKeyword( "VERSION"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextToken():
                raise Warning("expected version At Line %d" % self.CurrentLineNumber)
            section = VerSection.VerSection()
            section.Alignment = alignment
            section.BuildNum = buildNum
            if self.__Token.startswith("\"") or self.__Token.startswith("L\""):
                section.StringData = self.__Token
            else:
                section.FileName = self.__Token
            obj.SectionList.append(section)

        elif self.__IsKeyword( "UI"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextToken():
                raise Warning("expected UI At Line %d" % self.CurrentLineNumber)
            section = UiSection.UiSection()
            section.Alignment = alignment
            if self.__Token.startswith("\"") or self.__Token.startswith("L\""):
                section.StringData = self.__Token
            else:
                section.FileName = self.__Token
            obj.SectionList.append(section)
            
        elif self.__IsKeyword( "FV_IMAGE"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextWord():
                raise Warning("expected FV name At Line %d" % self.CurrentLineNumber)
            
            fvName = self.__Token.upper()
            fv = None
#            if not self.__IsToken( "{"):
#                raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)
            if self.__IsToken( "{"):
                fv = Fv.FV()
                fv.UiFvName = fvName
                self.__GetFvAlignment( fv)
                self.__GetFvAttributes( fv)
                self.__GetAprioriSection( fv)
    
                while True:
                    isInf = self.__GetInfStatement( fv)
                    isFile = self.__GetFileStatement( fv)
                    if not isInf and not isFile:
                        break
    
                if not self.__IsToken( "}"):
                    raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
            
            section = FvImageSection.FvImageSection()
            section.Alignment = alignment
            if fv != None:
                section.Fv = fv
                section.FvName = None
            else:
                section.FvName = fvName
                
            obj.SectionList.append(section) 
           
        else:
            
            if not self.__GetNextWord():
                raise Warning("expected section type At Line %d" % self.CurrentLineNumber)
            
            # Encapsulation section appear, UndoToken and return
            if self.__Token == "COMPRESS" or self.__Token == "GUIDED":
                self.SetFileBufferPos(oldPos)
                return False
            
            # DataSection
            section = DataSection.DataSection()
            section.Alignment = alignment
            section.SecType = self.__Token
            
            if self.__IsToken("="):
                if not self.__GetNextToken():
                    raise Warning("expected section file path At Line %d" % self.CurrentLineNumber)
                section.SectFileName = self.__Token
            else:
                if not self.__GetCglSection(section):
                    return False
            
            obj.SectionList.append(section)
            
        return True
            
    def __GetCglSection(self, obj, alignment = None):
        
        if self.__IsKeyword( "COMPRESS"):
            type = "PI_STD"
            if self.__IsKeyword("PI_STD") or self.__IsKeyword("PI_NONE"):
                type = self.__Token
                
            if not self.__IsToken("{"):
                raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)

            section = CompressSection.CompressSection()
            section.Alignment = alignment
            section.CompType = type
            # Recursive sections...
            while True:
                isLeafSection = self.__GetLeafSection(section)
                isEncapSection = self.__GetEncapsulationSec(section)
                if not isLeafSection and not isEncapSection:
                    break
            
            
            if not self.__IsToken( "}"):
                raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
            obj.SectionList.append(section)
                
#            else:
#               raise Warning("Compress type not known At Line %d" % self.CurrentLineNumber) 
           
            return True
        
        elif self.__IsKeyword( "GUIDED"):
            guid = None
            if self.__GetNextGuid():
                guid = self.__Token

            attribDict = self.__GetGuidAttrib()
            if not self.__IsToken("{"):
                raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)
            section = GuidSection.GuidSection()
            section.Alignment = alignment
            section.NameGuid = guid
            section.SectionType = "GUIDED"
            section.ProcessRequired = attribDict["PROCESSING_REQUIRED"]
            section.AuthStatusValid = attribDict["AUTH_STATUS_VALID"]
            # Recursive sections...
            while True:
                isLeafSection = self.__GetLeafSection(section)
                isEncapSection = self.__GetEncapsulationSec(section)
                if not isLeafSection and not isEncapSection:
                    break
            
            if not self.__IsToken( "}"):
                raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
            obj.SectionList.append(section)
                
            return True
        
        return False

    def __GetGuidAttrib(self):
        
        attribDict = {}
        attribDict["PROCESSING_REQUIRED"] = False
        attribDict["AUTH_STATUS_VALID"] = False
        if self.__IsKeyword("PROCESSING_REQUIRED") or self.__IsKeyword("AUTH_STATUS_VALID"):
            attrib = self.__Token

            if not self.__IsToken("="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
            if not self.__GetNextToken() or self.__Token.upper() not in ("TRUE", "FALSE", "1", "0"):
                raise Warning("expected TRUE/FALSE (1/0) At Line %d" % self.CurrentLineNumber)
            attribDict[attrib] = self.__Token
            
        if self.__IsKeyword("PROCESSING_REQUIRED") or self.__IsKeyword("AUTH_STATUS_VALID"):
            attrib = self.__Token

            if not self.__IsToken("="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

            if not self.__GetNextToken() or self.__Token.upper() not in ("TRUE", "FALSE", "1", "0"):
                raise Warning("expected TRUE/FALSE (1/0) At Line %d" % self.CurrentLineNumber)
            attribDict[attrib] = self.__Token
            
        return attribDict
            
    def __GetEncapsulationSec(self, ffsFile):        
        
        if not self.__IsKeyword( "SECTION"):
            if len(ffsFile.SectionList) == 0:
                raise Warning("expected SECTION At Line %d" % self.CurrentLineNumber)
            else:
                return False
        
        alignment = None
        if self.__GetAlignment():
            alignment = self.__Token
            
        return self.__GetCglSection(ffsFile, alignment)    

    def __GetCapsule(self):
        
        if not self.__GetNextToken():
            return False

        S = self.__Token.upper()
        if S.startswith("[") and not S.startswith("[CAPSULE."):
            if not S.startswith("[VTF.") and not S.startswith("[RULE."):
                raise Warning("Unknown section or section appear sequence error At Line %d.\n \
                            The correct sequence should be [FD.], [FV.], [Capsule.], [VTF.], [Rule.]" % self.CurrentLineNumber)
            self.__UndoToken()
            return False

        self.__UndoToken()
        if not self.__IsToken("[CAPSULE.", True):
            raise Warning("expected [Capsule.] At Line %d" % self.CurrentLineNumber)        
            
#        if not self.__IsToken("."):
#            raise Warning("expected '.' At line %d" % self.CurrentLineNumber)
        
        if not self.__SkipToToken("UEFI") and not self.__SkipToToken("FRAMEWORK"):
            raise Warning("expected Spec (UEFI | FRAMEWORK) At line %d" % self.CurrentLineNumber)
        
        capsule = Capsule.Capsule()
        capsule.SpecName = self.__SkippedChars
        
        if not self.__IsToken("."):
            raise Warning("expected '.' At line %d" % self.CurrentLineNumber)
        
        capsuleName = self.__GetUiName()
        if not capsuleName:
            raise Warning("expected capsule name At line %d" % self.CurrentLineNumber)
        
        capsule.UiCapsuleName = capsuleName.upper()
        
        if not self.__IsToken( "]"):
            raise Warning("expected ']' At Line %d" % self.CurrentLineNumber)
        
        if self.__IsKeyword("OUTFILE"):
            if not self.__IsToken( "="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            
            if not self.__GetNextToken():
                raise Warning("expected file name At Line %d" % self.CurrentLineNumber)
            
            capsule.CreateFile = self.__Token
        
        if self.__IsToken("<Capsule."):
            if not self.__GetDecimalNumber():
                raise Warning("expected Group ID number At Line %d" % self.CurrentLineNumber)
            capsule.GroupIdNumber = self.__Token
            
            if not self.__IsToken( ">"):
                raise Warning("expected '>' At Line %d" % self.CurrentLineNumber)
            
        self.__GetCapsuleStatements(capsule)
        self.profile.CapsuleList.append(capsule)
        return True    
            
    def __GetCapsuleStatements(self, capsule):
        
        self.__GetDefineStatements(capsule)
        self.__GetSetStatements(capsule)
        
        self.__GetTokens(capsule)
        capsuleData = CapsuleData.CapsuleData()
        capsule.CapsuleData = capsuleData
        self.__GetCapsuleData(capsule)
                
    def __GetTokens(self, capsule):
        
        while self.__CurrentLine().find("=") != -1:
            NameValue = self.__CurrentLine().split("=")
            capsule.TokensDict[NameValue[0].strip()] = NameValue[1].strip()
            self.CurrentLineNumber += 1
            self.CurrentOffsetWithinLine = 0
    
    def __GetCapsuleData(self, capsule):
        
        while self.__GetInfStatement(capsule.CapsuleData):
            pass

        while self.__GetFileStatement(capsule.CapsuleData):
            pass
        
        while self.__GetFvStatement(capsule):
            pass
    
    def __GetFvStatement(self, capsule):
        
        if not self.__IsKeyword("FV"):
            return False
        
        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetNextToken():
            raise Warning("expected FV name At Line %d" % self.CurrentLineNumber)
        
        capsule.CapsuleData.FvStatementList.append(self.__Token)
        return True
    
    def __GetRule(self):
        
        if not self.__GetNextToken():
            return False

        S = self.__Token.upper()
        if S.startswith("[") and not S.startswith("[RULE."):
            raise Warning("Unknown section or section appear sequence error At Line %d.\n \
                            The correct sequence should be [FD.], [FV.], [Capsule.], [VTF.], [Rule.]" % self.CurrentLineNumber)
#            self.__UndoToken()
#            return False

        self.__UndoToken()
        if not self.__IsToken("[Rule.", True):
            raise Warning("expected [Rule.] At Line %d" % self.CurrentLineNumber)

        if not self.__SkipToToken("."):
            raise Warning("expected '.' At Line %d" % self.CurrentLineNumber)
        
        arch = self.__SkippedChars.rstrip(".")
        if arch.upper() not in ("IA32", "X64", "IPF", "EBC", "COMMON"):
            raise Warning("Unknown Arch At line %d" % self.CurrentLineNumber)
        
        moduleType = self.__GetModuleType()
        
        templateName = ""
        if self.__IsToken("."):
            if not self.__GetNextWord():
                raise Warning("expected template name At Line %d" % self.CurrentLineNumber)
            templateName = self.__Token
            
        if not self.__IsToken( "]"):
            raise Warning("expected ']' At Line %d" % self.CurrentLineNumber)
        
        rule = self.__GetProcessFormat()
        rule.Arch = arch.upper()
        rule.ModuleType = moduleType
        rule.TemplateName = templateName
        if templateName == '' :
            self.profile.RuleDict['RULE'             + \
                              '.'                    + \
                              arch.upper()           + \
                              '.'                    + \
                              moduleType.upper()     ] = rule
        else :
            self.profile.RuleDict['RULE'             + \
                              '.'                    + \
                              arch.upper()           + \
                              '.'                    + \
                              moduleType.upper()     + \
                              '.'                    + \
                              templateName.upper() ] = rule
#        self.profile.RuleList.append(rule)
        return True
    
    def __GetModuleType(self):
        
        if not self.__GetNextWord():
            raise Warning("expected Module type At Line %d" % self.CurrentLineNumber)
        if self.__Token.upper() not in ("SEC", "PEI_CORE", "PEIM", "DXE_CORE", \
                             "DXE_DRIVER", "DXE_SAL_DRIVER", \
                             "DXE_SMM_DRIVER", "DXE_RUNTIME_DRIVER", \
                             "UEFI_DRIVER", "UEFI_APPLICATION", "USER", "DEFAULT"):
            raise Warning("Unknown Module type At line %d" % self.CurrentLineNumber)
        return self.__Token
        
    def __GetProcessFormat(self):
        
        if not self.__IsKeyword("FILE"):
            raise Warning("expected FILE At Line %d" % self.CurrentLineNumber)
        
        if not self.__GetNextWord():
            raise Warning("expected FV type At Line %d" % self.CurrentLineNumber)
        
        if self.__Token.strip().upper() not in ("SEC", "RAW", "FREEFORM", "DXE_CORE", \
                             "PEI_DXE_COMBO", "FV_IMAGE", \
                             "DRIVER", "APPLICATION", "PEI_CORE", "PEIM"):
            raise Warning("Unknown FV type At line %d" % self.CurrentLineNumber)
        
        type = self.__Token.strip().upper()

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
        
        if not self.__IsKeyword("$(NAMED_GUID)"):
            raise Warning("expected $(NAMED_GUID) At Line %d" % self.CurrentLineNumber)
#        guid = self.__Token
        
        fixed = False
        if self.__IsKeyword("Fixed", True):
            fixed = True
            
        checksum = False
        if self.__IsKeyword("CheckSum", True):
            checksum = True
            
        alignment = ""
        if self.__IsKeyword("Align", True):
            if not self.__IsToken("="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
            if not self.__GetNextToken():
                raise Warning("expected alignment value At Line %d" % self.CurrentLineNumber)
            if self.__Token not in ("8", "16", "32", "4K", "32K" ,"64K"):
                raise Warning("Incorrect alignment At Line %d" % self.CurrentLineNumber)
            alignment = self.__Token

        if self.__IsToken("{"):
            # Complex file rule expected
            rule = RuleComplexFile.RuleComplexFile()
            rule.FvType = type
            rule.Alignment = alignment
            rule.CheckSum = checksum
            rule.Fixed = fixed
            while self.__GetEfiSection(rule):
                pass

            self.__GetRuleEncapsulationSection(rule)
            
            while self.__GetEfiSection(rule, True):
                pass
            
            if not self.__IsToken("}"):
                raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
            
            return rule
        
        else:
            # Simple file rule expected
            if not self.__GetNextToken():
                raise Warning("expected File name At Line %d" % self.CurrentLineNumber)
            
            rule = RuleSimpleFile.RuleSimpleFile()
#            rule.NameGuid = guid
            rule.FvType = type
            rule.Alignment = alignment
            rule.CheckSum = checksum
            rule.Fixed = fixed
            rule.FileName = self.__Token
            return rule
        
        return Rule.Rule()

    def __GetEfiSection(self, obj, checkLeafArgs = False):
        
        oldPos = self.GetFileBufferPos()
        if not self.__GetNextWord():
#            raise Warning("expected EFI section name At Line %d" % self.CurrentLineNumber)
            return False
        sectionName = self.__Token
        
        if sectionName not in ("PE32", "PIC", "TE", "DXE_DEPEX", "VERSION", "UI", "COMPAT16", "FV_IMAGE", \
                                "FREEFORM_SUBTYPE_GUID", "RAW", "PEI_DEPEX"):
                                    self.__UndoToken()
                                    return False

        section = EfiSection.EfiSection()
        section.SectionType = sectionName
        
        if self.__IsKeyword("Optional"):
            section.Optional = True

        if checkLeafArgs:
            if self.__IsKeyword("BUILD_NUM"):
                if not self.__IsToken("="):
                    raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)
                if not self.__GetNextToken():
                    raise Warning("expected Build number At Line %d" % self.CurrentLineNumber)
                section.BuildNum = self.__Token
                
            if self.__GetAlignment():
                section.Alignment = self.__Token
                
        #        Leaf section encountered, restore to the beginning of section.
        if self.__IsKeyword("BUILD_NUM") or self.__IsKeyword("Align"):
            self.SetFileBufferPos(oldPos)
            return False
        
        if not self.__GetNextToken():
            raise Warning("expected EFI section File At Line %d" % self.CurrentLineNumber)
        section.Filename = self.__Token
        obj.SectionList.append(section)
        
        return True
        
        
    def __GetRuleEncapsulationSection(self, rule):

        if self.__IsKeyword( "COMPRESS"):
            type = "PI_STD"
            if self.__IsKeyword("PI_STD") or self.__IsKeyword("PI_NONE"):
                type = self.__Token
                
            if not self.__IsToken("{"):
                raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)

            section = CompressSection.CompressSection()
            
            section.CompType = type
            # Recursive sections...
            while self.__GetEfiSection(section):
                pass
            while self.__GetEfiSection(section, True):
                pass
            self.__GetRuleEncapsulationSection(section)
            
            if not self.__IsToken( "}"):
                raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
            rule.SectionList.append(section)
                
#            else:
#               raise Warning("Compress type not known At Line %d" % self.CurrentLineNumber) 
           
            return True

        elif self.__IsKeyword( "GUIDED"):
            guid = None
            if self.__GetNextGuid():
                guid = self.__Token
            attribDict = self.__GetGuidAttrib()
            
            if not self.__IsToken("{"):
                raise Warning("expected '{' At Line %d" % self.CurrentLineNumber)
            section = GuidSection.GuidSection()
            section.NameGuid = guid
            section.SectionType = "GUIDED"
            section.ProcessRequired = attribDict["PROCESSING_REQUIRED"]
            section.AuthStatusValid = attribDict["AUTH_STATUS_VALID"]
            
            # Efi sections...
            while self.__GetEfiSection(section):
                pass
            while self.__GetEfiSection(section, True):
                pass
            self.__GetRuleEncapsulationSection(section)
            
            if not self.__IsToken( "}"):
                raise Warning("expected '}' At Line %d" % self.CurrentLineNumber)
            rule.SectionList.append(section)

            return True

        return False
        
    def __GetVtf(self):
        
        if not self.__GetNextToken():
            return False

        S = self.__Token.upper()
        if S.startswith("[") and not S.startswith("[VTF."):
            if not S.startswith("[RULE."):
                raise Warning("Unknown section or section appear sequence error At Line %d.\n \
                            The correct sequence should be [FD.], [FV.], [Capsule.], [VTF.], [Rule.]" % self.CurrentLineNumber)
            self.__UndoToken()
            return False

        self.__UndoToken()
        if not self.__IsToken("[VTF.", True):
            raise Warning("expected [VTF.] At Line %d" % self.CurrentLineNumber)

        if not self.__SkipToToken("."):
            raise Warning("expected '.' At Line %d" % self.CurrentLineNumber)

        arch = self.__SkippedChars.rstrip(".").upper()
        if arch not in ("IA32", "X64", "IPF"):
            raise Warning("Unknown Arch At line %d" % self.CurrentLineNumber)

        if not self.__GetNextWord():
            raise Warning("expected VTF name At Line %d" % self.CurrentLineNumber)
        name = self.__Token.upper()

        vtf = Vtf.Vtf()
        vtf.UiName = name
        vtf.KeyArch = arch
        
        if self.__IsToken(","):
            if not self.__GetNextWord():
                raise Warning("expected Arch list At Line %d" % self.CurrentLineNumber)
            if self.__Token.upper() not in ("IA32", "X64", "IPF"):
                raise Warning("Unknown Arch At line %d" % self.CurrentLineNumber)
            vtf.ArchList = self.__Token.upper()

        if not self.__IsToken( "]"):
            raise Warning("expected ']' At Line %d" % self.CurrentLineNumber)
        
        if self.__IsKeyword("IA32_RST_BIN"):
            if not self.__IsToken("="):
                raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

            if not self.__GetNextToken():
                raise Warning("expected Reset file At Line %d" % self.CurrentLineNumber)

            vtf.ResetBin = self.__Token
            
        while self.__GetComponentStatement(vtf):
            pass
        
        self.profile.VtfList.append(vtf)
        return True
    
    def __GetComponentStatement(self, vtf):
        
        if not self.__IsKeyword("COMP_NAME"):
            return False
        
        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextWord():
            raise Warning("expected Component Name At Line %d" % self.CurrentLineNumber)

        compStatement = ComponentStatement.ComponentStatement()
        compStatement.CompName = self.__Token
        
        if not self.__IsKeyword("COMP_LOC"):
            raise Warning("expected COMP_LOC At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextWord():
            raise Warning("expected Component location At Line %d" % self.CurrentLineNumber)
        if self.__Token not in ("F", "N", "S", "H", "L", "PH", "PL"):
            raise Warning("Unknown location type At line %d" % self.CurrentLineNumber)
        compStatement.CompLoc = self.__Token
        
        if not self.__IsKeyword("COMP_TYPE"):
            raise Warning("expected COMP_TYPE At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextToken():
            raise Warning("expected Component type At Line %d" % self.CurrentLineNumber)
        if self.__Token not in ("FIT", "PAL_B", "PAL_A", "OEM"):
            if not self.__Token.startswith("0x") or len(self.__Token) < 3 or len(self.__Token) > 4 or \
                not self.__HexDigit(self.__Token[2]) or not self.__HexDigit(self.__Token[-1]):
                raise Warning("Unknown location type At line %d" % self.CurrentLineNumber)
        compStatement.CompType = self.__Token
        
        if not self.__IsKeyword("COMP_VER"):
            raise Warning("expected COMP_VER At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextToken():
            raise Warning("expected Component version At Line %d" % self.CurrentLineNumber)

        p = re.compile('-$|[0-9]{0,1}[0-9]{1}\.[0-9]{0,1}[0-9]{1}')
        if p.match(self.__Token) == None:
            raise Warning("Unknown version format At line %d" % self.CurrentLineNumber)
        compStatement.CompVer = self.__Token
        
        if not self.__IsKeyword("COMP_CS"):
            raise Warning("expected COMP_CS At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextToken():
            raise Warning("expected Component CS At Line %d" % self.CurrentLineNumber)
        if self.__Token not in ("1", "0"):
            raise Warning("Unknown  Component CS At line %d" % self.CurrentLineNumber)
        compStatement.CompCs = self.__Token
        
        
        if not self.__IsKeyword("COMP_BIN"):
            raise Warning("expected COMP_BIN At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextToken():
            raise Warning("expected Component file At Line %d" % self.CurrentLineNumber)

#        p = re.compile('-$|\\.bin$')
#        if p.match(self.__Token.strip()) == None:
#            raise Warning("Unknown file name At line %d" % self.CurrentLineNumber)
        compStatement.CompBin = self.__Token
        
        if not self.__IsKeyword("COMP_SYM"):
            raise Warning("expected COMP_SYM At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if not self.__GetNextToken():
            raise Warning("expected Component symbol file At Line %d" % self.CurrentLineNumber)

#        p = re.compile('-$|\.sym$')
#        if p.match(self.__Token.strip()) == None:
#            raise Warning("Unknown file name At line %d" % self.CurrentLineNumber)
        compStatement.CompSym = self.__Token
    
        if not self.__IsKeyword("COMP_SIZE"):
            raise Warning("expected COMP_SIZE At Line %d" % self.CurrentLineNumber)

        if not self.__IsToken("="):
            raise Warning("expected '=' At Line %d" % self.CurrentLineNumber)

        if self.__IsToken("-"):
            compStatement.CompSize = self.__Token
        elif self.__GetDecimalNumber():
            compStatement.CompSize = self.__Token
        elif self.__GetHexNumber():
            compStatement.CompSize = self.__Token
        else:
            raise Warning("Unknown size At line %d" % self.CurrentLineNumber)
        
        vtf.ComponentStatementList.append(compStatement)
        return True
    
if __name__ == "__main__":
    parser = FdfParser("Nt32.fdf")
    parser.ParseFile()
    print "Success!"

