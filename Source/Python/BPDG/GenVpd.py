## @file
#  This file include GenVpd class for fix the Vpd type PCD offset, and PcdEntry for describe
#  and process each entry of vpd type PCD.
#
#  Copyright (c) 2010, Intel Corporation. All rights reserved.<BR>
#
#  This program and the accompanying materials
#  are licensed and made available under the terms and conditions of the BSD License
#  which accompanies this distribution.  The full text of the license may be found at
#  http://opensource.org/licenses/bsd-license.php
#
#  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
#  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

import os
import StringIO
import StringTable as st
import array

from struct import *
import Common.EdkLogger as EdkLogger
import Common.BuildToolError as BuildToolError

_FORMAT_CHAR = {1: 'B',
                2: 'H',
                4: 'I',
                8: 'Q'
                }

class PcdEntry:
    def __init__(self, PcdCName, PcdOffset, PcdSize, PcdValue, PcdUnpackValue=None, 
                 PcdBinOffset=None, PcdBinSize=None):
        self.PcdCName       = PcdCName.strip()
        self.PcdOffset      = PcdOffset.strip()
        self.PcdSize        = PcdSize.strip()
        self.PcdValue       = PcdValue.strip()
        self.PcdUnpackValue = PcdUnpackValue
        self.PcdBinOffset   = PcdBinOffset
        self.PcdBinSize     = PcdBinSize
        
        if self.PcdValue == '' :
            EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, "Invalid PCD format, no Value specified!")
                         
        if self.PcdOffset == '' :
            EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, "Invalid PCD format, no Offset specified!")
            
        if self.PcdSize == '' :
            EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, "Invalid PCD format, no PcdSize specified!")  
                   
        self._GenOffsetValue ()
        
    def _IsBoolean(self, ValueString):
        if ValueString.upper() in ["TRUE", "FALSE"]:
            return True
        return False
    
    def _GenOffsetValue(self):
        if self.PcdOffset != "*" :
            try:
                self.PcdBinOffset = int (self.PcdOffset)
            except:
                try:
                    self.PcdBinOffset = int(self.PcdOffset, 16)
                except:
                    EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, 
                                    "Invalid offset value %s for PCD %s" % (self.PcdOffset, self.PcdCName))                                  
        
    def _PackBooleanValue(self, ValueString):
        if ValueString.upper() == "TRUE":
            self.PcdValue =  pack(_FORMAT_CHAR[1], 1)
        else:
            self.PcdValue =  pack(_FORMAT_CHAR[1], 0)
                
    def _PackIntValue(self, IntValue, Size):
        if Size not in _FORMAT_CHAR.keys():
            EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, 
                            "Invalid size %d for PCD in integer datum size." % Size)        
        self.PcdValue =  pack(_FORMAT_CHAR[Size], IntValue)
        
    def _PackPtrValue(self, ValueString, Size):
        if ValueString.startswith('L"'):
            self._PackUnicode(ValueString, Size)
        elif ValueString.startswith('{') and ValueString.endswith('}'):
            self._PackByteArray(ValueString, Size)
        elif ValueString.startswith('"') and ValueString.endswith('"'):
            self._PackString(ValueString, Size)
        else:
            EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, 
                            "Invalid VOID* type PCD value %s" % ValueString) 
                   
    def _PackString(self, ValueString, Size):
        assert Size > 0, "Invalid parameter Size!"
        assert ValueString != "", "Invalid parameter ValueString"
        assert len(ValueString) >= 2, 'An ASCII string at least contains two "'
        
        ValueString = ValueString[1:-1]
        if len(ValueString) + 1 > Size:
            EdkLogger.error("BPDG", BuildToolError.RESOURCE_OVERFLOW, 
                            "PCD value string %s is exceed to size %d" % (ValueString, Size))
        self.PcdValue=  pack('%ds' % Size, ValueString)
        
    def _PackByteArray(self, ValueString, Size):
        assert Size > 0, "Invalid parameter Size!"
        assert ValueString != "", "Invalid parameter ValueString"
        
        ValueString = ValueString.strip()
        ValueString = ValueString.lstrip('{').strip('}')
        ValueList = ValueString.split(',')
        ValueList = [item.strip() for item in ValueList]
        
        if len(ValueList) > Size:
            EdkLogger.error("BPDG", BuildToolError.RESOURCE_OVERFLOW, 
                            "The byte array %s is too large for size %d" % (ValueString, Size))
        
        ReturnArray = array.array('B')
        
        for Index in xrange(len(ValueList)):
            Value = None
            if ValueList[Index].startswith('0x'):
                # translate hex value
                try:
                    Value = int(ValueList[Index], 16)
                except:
                    EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, 
                                    "The value item %s in byte array %s is an invalid HEX value." % \
                                    (ValueList[Index], ValueString))
            else:
                # translate decimal value
                try:
                    Value = int(ValueList[Index], 10)
                except:
                    EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID,
                                    "The value item %s in byte array %s is an invalid DECIMAL value." % \
                                    (ValueList[Index], ValueString))
            
            if Value > 255:
                EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, 
                                "The value item %s in byte array %s do not in range 0 ~ 0xFF" %\
                                (ValueList[Index], ValueString))
             
            ReturnArray.append(Value)
            
        for Index in xrange(len(ValueList), Size):
            ReturnArray.append(0)
        
        self.PcdValue =  ReturnArray.tolist()

    ## Pack a unicode PCD value into byte array.
    #  
    #  A unicode string for a PCD should be in format as  L"".
    #
    def _PackUnicode(self, UnicodeString, Size):
        assert Size > 0, "Invalid parameter Size"
        assert len(UnicodeString) >= 3, "Invalid parameter UnicodeString"
        
        UnicodeString = UnicodeString[2:-1]
        
        if (len(UnicodeString) + 1) * 2 > Size:
            EdkLogger.error("BPDG", BuildToolError.RESOURCE_OVERFLOW,
                            "The size of unicode string %s is too larger for size %s" % \
                            (UnicodeString, Size))
            
        ReturnArray = array.array('B')
        for Value in UnicodeString:
            try:
                ReturnArray.append(ord(Value))
                ReturnArray.append(0)
            except:
                EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, 
                                "Invalid unicode character %s in unicode string %s" % \
                                (Value, UnicodeString))
                
        for Index in range(len(UnicodeString) * 2, Size):
            ReturnArray.append(0)
            
        self.PcdValue =  ReturnArray.tolist()    
        
class GenVPD :
    
    ## Constructor of DscBuildData
    #
    #  Initialize object of GenVPD
    #   @Param      InputFileName   The filename include the vpd type pcd information
    #   @param      MapFileName     The filename of map file that stores vpd type pcd information.
    #                               This file will be generated by the BPDG tool after fix the offset
    #                               and adjust the offset to make the pcd data aligned.
    #   @param      VpdFileName     The filename of Vpd file that hold vpd pcd information.
    #
    def __init__(self, InputFileName, MapFileName, VpdFileName):
        self.InputFileName           = InputFileName
        self.MapFileName             = MapFileName
        self.VpdFileName             = VpdFileName
        self.FileLinesList           = []
        self.PcdFixedOffsetSizeList  = []
        self.PcdUnknownOffsetList    = []
        try:
            fInputfile = open(InputFileName, "r", 0)
            try:
                self.FileLinesList = fInputfile.readlines()
            except:
                EdkLogger.error("BPDG", BuildToolError.FILE_READ_FAILURE, "File read failed for %s" %InputFileName,None)
            finally:
                fInputfile.close()
        except:
            EdkLogger.error("BPDG", BuildToolError.FILE_OPEN_FAILURE, "File open failed for %s" %InputFileName,None)
    
    ##
    # Parser the input file which is generated by the build tool. Convert the value of each pcd's 
    # from string to it's real format. Also remove the useless line in the input file.
    # 
    def ParserInputFile (self):
        count = 0        
        for line in self.FileLinesList:
            # Strip "\r\n" generated by readlines ().
            line = line.strip()
            line = line.rstrip(os.linesep)
                       
            # Skip the comment line
            if (not line.startswith("#")) and len(line) > 1 :              
                self.FileLinesList[count] = line.split('|')
            elif len(line) <= 1 :
                # Set the blank line to "None"
                self.FileLinesList[count] = None
            else :
                # Set the comment line to "None"
                self.FileLinesList[count] = None
            count += 1
            
        # The line count contain usage information
        count = 0     
        # Delete useless lines
        while (True) :
            try :
                if (self.FileLinesList[count] == None) :
                    del(self.FileLinesList[count])
                else :
                    count += 1
            except :
                break     
        #
        # After remove the useless line, if there are no data remain in the file line list,
        # Report warning messages to user's.
        # 
        if len(self.FileLinesList) == 0 :
            EdkLogger.warn('BPDG', BuildToolError.RESOURCE_NOT_AVAILABLE, 
                           "There are no VPD type pcds defined in DSC file, Please check it.")
                      
        # Process the pcds one by one base on the pcd's value and size
        count = 0
        for line in self.FileLinesList:        
            if line != None :
                PCD = PcdEntry(line[0], line[1], line[2], line[3])   
                # Strip the space char
                PCD.PcdCName     = PCD.PcdCName.strip(' ')
                PCD.PcdOffset    = PCD.PcdOffset.strip(' ')
                PCD.PcdSize      = PCD.PcdSize.strip(' ')
                PCD.PcdValue     = PCD.PcdValue.strip(' ')               
                                      
                #
                # Store the original pcd value.
                # This information will be useful while generate the output map file.
                #
                PCD.PcdUnpackValue    =  str(PCD.PcdValue)                              

                #
                # Translate PCD size string to an integer value.
                PackSize = None
                try:
                    PackSize = int(PCD.PcdSize, 10)
                    PCD.PcdBinSize = PackSize
                except:
                    try:
                        PackSize = int(PCD.PcdSize, 16)
                        PCD.PcdBinSize = PackSize
                    except:
                        EdkLogger.error("BPDG", BuildToolError.FORMAT_INVALID, "Invalid PCD size value %s" % PCD.PcdSize)
                    
                if PCD._IsBoolean(PCD.PcdValue):
                    PCD._PackBooleanValue(PCD.PcdValue)
                    self.FileLinesList[count] = PCD
                    count += 1
                    continue
                #
                # Try to translate value to an integer firstly.
                #
                IsInteger = True
                PackValue  = None
                try:
                    PackValue = int(PCD.PcdValue)
                except:
                    try:
                        PackValue = int(PCD.PcdValue, 16)
                    except:
                        IsInteger = False
                
                if IsInteger:
                    PCD._PackIntValue(PackValue, PackSize)
                else:
                    PCD._PackPtrValue(PCD.PcdValue, PackSize)
                    
                self.FileLinesList[count] = PCD
                count += 1
            else :
                continue
            
    ##
    # This function used to create a clean list only contain useful information and reorganized to make it 
    # easy to be sorted
    #
    def FormatFileLine (self) :
             
        for eachPcd in self.FileLinesList :
            if eachPcd.PcdOffset != '*' :
                # Use pcd's Offset value as key, and pcd's Value as value 
                self.PcdFixedOffsetSizeList.append(eachPcd)
            else :
                # Use pcd's CName as key, and pcd's Size as value
                self.PcdUnknownOffsetList.append(eachPcd)
                                        
                            
    ##
    # This function is use to fix the offset value which the not specified in the map file.
    # Usually it use the star (meaning any offset) character in the offset field
    #    
    def FixVpdOffset (self):        
        # At first, the offset should start at 0
        # Sort fixed offset list in order to find out where has free spaces for the pcd's offset
        # value is "*" to insert into.      
        
        self.PcdFixedOffsetSizeList.sort(lambda x,y: cmp(x.PcdBinOffset, y.PcdBinOffset))                            
                
        #
        # Sort the un-fixed pcd's offset by it's size.
        #
        self.PcdUnknownOffsetList.sort(lambda x,y: cmp(x.PcdBinSize, y.PcdBinSize))
        
        # Check the offset of VPD type pcd's offset start from 0.    
        if self.PcdFixedOffsetSizeList[0].PcdBinOffset  != 0 :
            EdkLogger.warn("BPDG", "The offset of VPD type pcd should start with 0, please check it.",
                            None)  
            
        # Judge whether the offset in fixed pcd offset list is overlapped or not.
        lenOfList = len(self.PcdFixedOffsetSizeList)
        count     = 0                       
        while (count < lenOfList - 1) :
            PcdNow  = self.PcdFixedOffsetSizeList[count]
            PcdNext = self.PcdFixedOffsetSizeList[count+1]
            # Two pcd's offset is same            
            if PcdNow.PcdBinOffset == PcdNext.PcdBinOffset :
                EdkLogger.error("BPDG", BuildToolError.ATTRIBUTE_GET_FAILURE, 
                                "The offset of %s is same with %s" % (PcdNow.PcdCName, PcdNext.PcdCName),
                                None)
            
            # Overlapped   
            if PcdNow.PcdBinOffset + PcdNow.PcdBinSize > PcdNext.PcdBinOffset :
                EdkLogger.error("BPDG", BuildToolError.ATTRIBUTE_GET_FAILURE, 
                                "The offset of %s is overlapped with %s" % (PcdNow.PcdCName, PcdNext.PcdCName),
                                None)
                
            # Has free space, raise a warning message   
            if PcdNow.PcdBinOffset + PcdNow.PcdBinSize < PcdNext.PcdBinOffset :
                EdkLogger.warn("BPDG", BuildToolError.ATTRIBUTE_GET_FAILURE, 
                               "The offsets have free space of between %s and %s" % (PcdNow.PcdCName, PcdNext.PcdCName),
                                None)
            count += 1
                             
        LastOffset              = self.PcdFixedOffsetSizeList[0].PcdBinOffset
        FixOffsetSizeListCount  = 0
        lenOfList               = len(self.PcdFixedOffsetSizeList)
        lenOfUnfixedList        = len(self.PcdUnknownOffsetList)
                
        ##
        # Insert the un-fixed offset pcd's list into fixed offset pcd's list if has free space between those pcds. 
        # 
        while (FixOffsetSizeListCount < lenOfList) :
            
            eachFixedPcd     = self.PcdFixedOffsetSizeList[FixOffsetSizeListCount]                       
            NowOffset        = eachFixedPcd.PcdBinOffset
            
            # Has free space               
            if LastOffset < NowOffset :
                if lenOfUnfixedList != 0 :
                    countOfUnfixedList = 0
                    while(countOfUnfixedList < lenOfUnfixedList) :                   
                        #needFixPcdCName, needFixPcdOffset, needFixPcdSize, needFixPcdValue, needFixUnpackValue = self.PcdUnknownOffsetList[countOfUnfixedList][0:6]
                        eachUnfixedPcd      = self.PcdUnknownOffsetList[countOfUnfixedList]
                        needFixPcdSize      = eachUnfixedPcd.PcdBinSize
                        needFixPcdOffset    = eachUnfixedPcd.PcdOffset
                        # Not been fixed
                        if eachUnfixedPcd.PcdOffset == '*' :
                            # The offset un-fixed pcd can write into this free space
                            if needFixPcdSize <= (NowOffset - LastOffset) :
                                # Change the offset value of un-fixed pcd
                                eachUnfixedPcd.PcdOffset    = str(hex(LastOffset))
                                eachUnfixedPcd.PcdBinOffset = LastOffset
                                # Insert this pcd into fixed offset pcd list.
                                self.PcdFixedOffsetSizeList.insert(FixOffsetSizeListCount,eachUnfixedPcd)
                                
                                # Delete the item's offset that has been fixed and added into fixed offset list
                                self.PcdUnknownOffsetList.pop(countOfUnfixedList)
                                
                                # After item added, should enlarge the length of fixed pcd offset list
                                lenOfList               += 1                                
                                FixOffsetSizeListCount  += 1
                                
                                # Decrease the un-fixed pcd offset list's length
                                countOfUnfixedList      += 1
                                lenOfUnfixedList        -= 1
                                
                                # Modify the last offset value 
                                LastOffset              += needFixPcdSize
                                continue                            
                            else :
                                # It can not insert into those two pcds, need to check stiil has other space can store it.
                                FixOffsetSizeListCount += 1
                                break                   
                        else :
                            continue
                # Set the FixOffsetSizeListCount = lenOfList for quit the loop
                else :
                    FixOffsetSizeListCount = lenOfList                    
                        
            # No free space, smoothly connect with previous pcd. 
            elif LastOffset == NowOffset :
                LastOffset = NowOffset + eachFixedPcd.PcdBinSize
                FixOffsetSizeListCount += 1
            # Usually it will not enter into this thunk, if so, means it overlapped. 
            else :
                EdkLogger.error("BPDG", BuildToolError.ATTRIBUTE_NOT_AVAILABLE, 
                                "The offset value definition has overlapped at pcd: %s, it's offset is: %s" %(eachFixedPcd.PcdCName, eachFixedPcd.PcdOffset),
                                None)
                FixOffsetSizeListCount += 1
        
        # Continue to process the un-fixed offset pcd's list, add this time, just append them behind the fixed pcd's offset list.    
        lenOfUnfixedList  = len(self.PcdUnknownOffsetList)
        lenOfList         = len(self.PcdFixedOffsetSizeList)
        while (lenOfUnfixedList > 0) :
            # Still has items need to process
            # The last pcd instance
            LastPcd    = self.PcdFixedOffsetSizeList[lenOfList-1]
            NeedFixPcd = self.PcdUnknownOffsetList[0]
            
            NeedFixPcd.PcdBinOffset = LastPcd.PcdBinOffset + LastPcd.PcdBinSize
            NeedFixPcd.PcdOffset    = str(hex(NeedFixPcd.PcdBinOffset))
            
            # Insert this pcd into fixed offset pcd list's tail.
            self.PcdFixedOffsetSizeList.insert(lenOfList, NeedFixPcd)
            # Delete the item's offset that has been fixed and added into fixed offset list
            self.PcdUnknownOffsetList.pop(0)
            
            lenOfList          += 1
            lenOfUnfixedList   -= 1                                                                                                                
    ##
    # Write the final data into output files.
    #   
    def GenerateVpdFile (self, MapFileName, BinFileName):
        #Open an VPD file to process

        try:
            fVpdFile  = open (BinFileName, "wb", 0)               
        except:
            # Open failed
            EdkLogger.error("BPDG", BuildToolError.FILE_OPEN_FAILURE, "File open failed for %s" %self.VpdFileName,None)
        
        try :
            fMapFile  = open (MapFileName, "w", 0)
        except:
            # Open failed
            EdkLogger.error("BPDG", BuildToolError.FILE_OPEN_FAILURE, "File open failed for %s" %self.MapFileName,None)
        
        # Use a instance of StringIO to cache data
        fStringIO = StringIO.StringIO('') 
        
        # Write the header of map file.
        try :
            fMapFile.write (st.MAP_FILE_COMMENT_TEMPLATE + "\n")
        except:
            EdkLogger.error("BPDG", BuildToolError.FILE_WRITE_FAILURE, "Write data to file %s failed, please check whether the file been locked or using by other applications." %self.MapFileName,None)  
                  
        for eachPcd in self.PcdFixedOffsetSizeList  :
            # write map file
            try :
                fMapFile.write("%s | %s | %s | %s  \n" % (eachPcd.PcdCName, eachPcd.PcdOffset, eachPcd.PcdSize,eachPcd.PcdUnpackValue))
            except:
                EdkLogger.error("BPDG", BuildToolError.FILE_WRITE_FAILURE, "Write data to file %s failed, please check whether the file been locked or using by other applications." %self.MapFileName,None)                                                                      
                         
            # Write Vpd binary file
            fStringIO.seek (eachPcd.PcdBinOffset)          
            if isinstance(eachPcd.PcdValue, list):
                ValueList = [chr(Item) for Item in eachPcd.PcdValue]
                fStringIO.write(''.join(ValueList))      
            else:                 
                fStringIO.write (eachPcd.PcdValue)
                                           
        try :  
            fVpdFile.write (fStringIO.getvalue())
        except:
            EdkLogger.error("BPDG", BuildToolError.FILE_WRITE_FAILURE, "Write data to file %s failed, please check whether the file been locked or using by other applications." %self.VpdFileName,None)
        
        fStringIO.close ()
        fVpdFile.close ()
        fMapFile.close ()
        
