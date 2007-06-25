# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to collect all defined strings in multiple uni files 
#

import codecs
import binascii
import os
import EdkLogger

def StrToUnix(Str):
    return unicode(Str)

def HexListToUni(List):
    pass

def UniToStr(Uni):
    return repr(Uni)[2:-1]

def UniToHexList(Uni):
    List = []
    HexNullStr = '0x00'
    for Item in Uni:
        DecNum = ord(Item)
        if DecNum < 16:
            HexStr = '0x0' + hex(DecNum)[2:].upper()
            List.append(HexStr)
            List.append(HexNullStr)
        elif DecNum < 256:
            HexStr = hex(DecNum).upper().replace('X' ,'x')
            List.append(HexStr)
            List.append(HexNullStr)
        elif DecNum < 4096:
            HexStr = hex(ord(Item))[2:].upper()
            List.append('0x'.join(HexStr[1:]))
            List.append('0x0'.join(HexStr[0:1]))
        else:
            HexStr = hex(DecNum).upper().replace('X' ,'x')
            List.append(HexStr)
    return List

class StringDefinitionClassObject(object):
    def __init__(self, Name = None, Language = None, Value = None, Token = None):
        self.StringName = ''
        self.StringNameByteList = []
        self.StringValue = {}                        #{ u'Language' : u'Value' }
        self.Referenced = False
        self.Offset = ''
        self.Token = ''
        
        if Name != None:
            self.StringName = Name
            self.StringNameByteList = UniToHexList(Name)
        if Value != None and Language != None:
            self.StringValue[Language] = UniToHexList(Value)
        if Token != None:
            self.Token = Token
        
    def Update(self, Name = None, Language = None, Value = None):
        if Name != None:
            self.StringName = Name
            self.StringNameByteList = UniToHexList(Name)
            
        if Value != None and Language != None:
            self.StringValue[Language] = UniToHexList(Value)
        
    def __str__(self):
        return repr(self.StringName) + ' ' + \
               repr(self.Token) + ' ' + \
               repr(self.Referenced) + ' ' + \
               repr(self.StringValue)

class UniFileClassObject(object):
    def __init__(self, FileList = []):
        self.FileList = FileList
        self.Token = 2
        self.LanguageDef = {}                   #{ u'LanguageIdentifier' : [PrintableName] }
        self.StringList = {}                    #{ 'StringName' : StringDefinitionClassObject }
        self.OrderedStringList = []               #[ StringDefinitionClassObject ] 
        
        if len(self.FileList) > 0:
            self.LoadUniFiles(FileList)
                
    def GetLangDef(self, Line):
        LangName = Line[Line.find(u'#langdef ') + len(u'#langdef ') : Line.find(u' ', len(u'#langdef '))]
        LangPrintName = Line[Line.find(u'\"') + len(u'\"') : Line.rfind(u'\"')]
        self.LanguageDef[LangName] = UniToHexList(LangPrintName)

        return True
        
    def GetStringObject(self, Item):
        Name = ''
        Language = ''
        Value = ''
        
        Name = Item[Item.find(u'#string ') + len(u'#string ') :Item.find(u' ', len(u'#string '))]
        LanguageList = Item.split(u'#language ')
        for IndexI in range(len(LanguageList)):
            if IndexI == 0:
                continue
            else:
                Language = LanguageList[IndexI][ : LanguageList[IndexI].find(u' ')]
                Value = LanguageList[IndexI][LanguageList[IndexI].find(u'\"') + len(u'\"') : LanguageList[IndexI].rfind(u'\"')].replace(u'\r\n', u'')
                self.AddStringToList(Name, Language, Value)
    
    def LoadUniFile(self, File = None):
        if File != None:
            if os.path.exists(File) and os.path.isfile(File):
                FileIn = codecs.open(File, mode='rb', encoding='utf-16').readlines()             
                Lines = []
                #
                # Use unique identifier
                #
                for Index in range(len(FileIn)):
                    if FileIn[Index].startswith(u'//') or FileIn[Index] == u'\r\n':
                        continue
                    FileIn[Index] = FileIn[Index].replace(u'/langdef', u'#langdef')
                    FileIn[Index] = FileIn[Index].replace(u'/string', u'#string')
                    FileIn[Index] = FileIn[Index].replace(u'/language', u'#language')
                    FileIn[Index] = FileIn[Index].replace(u'\t', u' ')
                    Lines.append(FileIn[Index])
                
                #
                # Get Unicode Information
                #
                for IndexI in range(len(Lines)):
                    Line = Lines[IndexI]
                    #
                    # Ignore comment line and empty line
                    #
                    if Line.startswith(u'//') or Line.strip() == u'\r\n':
                        continue
                    
                    if (IndexI + 1) < len(Lines):
                        SecondLine = Lines[IndexI + 1]
                    if (IndexI + 2) < len(Lines):
                        ThirdLine = Lines[IndexI + 2]
                                            
                    #
                    # Get Language def information
                    # 
                    if Line.find(u'#langdef ') >= 0:
                        self.GetLangDef(Line)
                        continue
                    
                    Name = ''
                    Language = ''
                    Value = ''
                    
                    #
                    # Get string def information format 1 as below
                    #
                    #     #string MY_STRING_1
                    #     #language eng
                    #     My first English string line 1
                    #     My first English string line 2
                    #     #string MY_STRING_1
                    #     #language spa
                    #     Mi segunda secuencia 1
                    #     Mi segunda secuencia 2
                    #
                    if Line.find(u'#string ') >= 0 and Line.find(u'#language ') < 0 and \
                        SecondLine.find(u'#string ') < 0 and SecondLine.find(u'#language ') >= 0 and \
                        ThirdLine.find(u'#string ') < 0 and ThirdLine.find(u'#language ') < 0:
                        Name = Line[Line.find(u'#string ') + len(u'#string ') : ].strip()
                        Language = SecondLine[SecondLine.find(u'#language ') + len(u'#language ') : ].strip()
                        for IndexJ in range(IndexI + 2, len(Lines)):
                            if Lines[IndexJ].find(u'#string ') < 0 and Lines[IndexJ].find(u'#language ') < 0:
                                Value = Value + Lines[IndexJ]
                            else:
                                IndexI = IndexJ
                                break
                        Value = Value.replace(u'\r\n', u'')
                        self.AddStringToList(Name, Language, Value)
                        continue
                    
                    #
                    # Get string def information format 2 as below
                    #
                    #     #string MY_STRING_1     #language eng     "My first English string line 1"
                    #                                               "My first English string line 2"
                    #                             #language spa     "Mi segunda secuencia 1"
                    #                                               "Mi segunda secuencia 2"
                    #     #string MY_STRING_2     #language eng     "My first English string line 1"
                    #                                               "My first English string line 2"
                    #     #string MY_STRING_2     #language spa     "Mi segunda secuencia 1"
                    #                                               "Mi segunda secuencia 2"
                    #
                    if Line.find(u'#string ') >= 0 and Line.find(u'#language ') >= 0:
                        StringItem = Line
                        for IndexJ in range(IndexI + 1, len(Lines)):
                            if Lines[IndexJ].find(u'#string ') >= 0 and Lines[IndexJ].find(u'#language ') >= 0:
                                IndexI = IndexJ
                                break
                            elif Lines[IndexJ].find(u'#string ') < 0 and Lines[IndexJ].find(u'#language ') >= 0:
                                StringItem = StringItem + Lines[IndexJ]
                            elif Lines[IndexJ].find(u'\"') >= 2:
                                StringItem = StringItem[ : StringItem.rfind(u'\"')] + Lines[IndexJ][Lines[IndexJ].find(u'\"') + len(u'\"') : ]
                        self.GetStringObject(StringItem)
                
                #
                # Add default string
                #
                for Language in self.LanguageDef.keys():
                    self.AddStringToList(u'$LANGUAGE_NAME', Language, Language, 0)
                    self.AddStringToList(u'$PRINTABLE_LANGUAGE_NAME', Language, self.LanguageDef[Language], 1)                

    def LoadUniFiles(self, FileList = []):
        if len(FileList) > 0:
            for File in FileList:
                self.LoadUniFile(File)
                
    def AddStringToList(self, Name, Language, Value, Token = None):
        if Name in self.StringList.keys():
            self.StringList[UniToStr(Name)].Update(Name, Language, Value)
        else:
            if Token != None:
                self.StringList[UniToStr(Name)] = StringDefinitionClassObject(Name, Language, Value, Token)
            else:
                self.StringList[UniToStr(Name)] = StringDefinitionClassObject(Name, Language, Value, self.Token)
                self.Token = self.Token + 1
            
    def FindStringObjectNameByToken(self, Token):
        for Item in self.StringList:
            if self.StringList[Item].Token == Token:
                return Item
        return None
    
    def SetStringReferenced(self, Name):
        if Name in self.StringList.keys():
            self.StringList[Name].Referenced = True
            
    
    def CreateOrderedStringList(self):
        pass
    
    def ReToken(self):
        Token = 2
        FalseCount = 1
        Length = len(self.StringList)
        for Index in range(2, Length):
            Name = self.FindStringObjectNameByToken(Index)
            if Name != None:
                if self.StringList[Name].Referenced == True:
                    self.StringList[Name].Token = Token
                    Token = Token + 1
                else:
                    self.StringList[Name].Token = Length + FalseCount
                    FalseCount = FalseCount + 1
                
        for Index in range(2, Length + FalseCount):
            Name = self.FindStringObjectNameByToken(Index)
            if Name != None and self.StringList[Name].Referenced == False:
                self.StringList[Name].Token = Token
                Token = Token + 1
            
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    a = UniFileClassObject(['C:\\Documents and Settings\\hchen30\\Desktop\\inventorystrings.uni'])
    for i in a.LanguageDef:
        print i, a.LanguageDef[i]
    for i in a.StringList:
        print i, str(a.StringList[i])
    