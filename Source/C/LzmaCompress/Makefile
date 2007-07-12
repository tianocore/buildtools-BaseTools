!INCLUDE ..\MSmakefile.common

APPNAME = LzmaCompress

#
# Target specific information
#

TARGET_NAME         = CustomizedCompress
TARGET_LIB          = $(TARGET_NAME).lib

LZMACFLAGS          = /I7zip\Src\7zip\Compress\LZMA_Alone /O2  \
                      /D "NDEBUG" /D "WIN32" /D "_CONSOLE" /D "_MBCS" /FD /Fd$(TARGET_NAME)Obj /EHsc \
                      /Yc"StdAfx.h" /Fp"AloneLZMA.pch" /c /W3 /TP

SRCFILES  = 7zip\Src\Misc\LzmaMain.cpp                  \
            7zip\Src\Misc\BufferStream.cpp              \
            7zip\Src\7zip\Common\OutBuffer.cpp          \
            7zip\Src\7zip\Common\InBuffer.cpp           \
            7zip\Src\7zip\Common\FileStreams.cpp        \
            7zip\Src\Common\Vector.cpp                  \
            7zip\Src\Common\StringToInt.cpp             \
            7zip\Src\Common\StringConvert.cpp           \
            7zip\Src\Common\String.cpp                  \
            7zip\Src\Common\NewHandler.cpp              \
            7zip\Src\Common\CRC.cpp                     \
            7zip\Src\Common\CommandLineParser.cpp       \
            7zip\Src\Common\CommandLineParser.h         \
            7zip\Src\Common\Alloc.cpp                   \
            7zip\Src\Windows\FileIO.cpp                 \
            7zip\Src\7zip\Compress\Lz\LZOutWindow.cpp   \
            7zip\Src\7zip\Compress\Lz\LZInWindow.cpp    \
            7zip\Src\7zip\Compress\RangeCoder\RangeCoderBit.cpp \
            7zip\Src\7zip\Compress\Lzma\LZMAEncoder.cpp \
            7zip\Src\7zip\Compress\Lzma\LZMADecoder.cpp             
          
OBJS = LzmaMain.obj BufferStream.obj OutBuffer.obj InBuffer.obj FileStreams.obj Vector.obj\
  StringToInt.obj StringConvert.obj String.obj NewHandler.obj CRC.obj CommandLineParser.obj Alloc.obj\
  FileIO.obj LZOutWindow.obj LZInWindow.obj RangeCoderBit.obj LZMAEncoder.obj LZMADecoder.obj

LIBS = Common.lib String.lib
  
OBJECTS = LzmaCompress.obj LzmaDecode.obj $(TARGET_LIB)
#OBJECTS = LzmaCompress.obj

!INCLUDE ..\MSmakefile.app

$(TARGET_LIB) : $(OBJS)
  $(AR) $(OBJS) /OUT:$(TARGET_LIB)
  
#
# Compile each source file
#
 
LzmaMain.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Misc\LzmaMain.cpp /Fo"LzmaMain.obj"
    
BufferStream.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Misc\BufferStream.cpp /Fo"BufferStream.obj"

OutBuffer.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Common\OutBuffer.cpp /Fo"OutBuffer.obj"
  
InBuffer.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Common\InBuffer.cpp /Fo"InBuffer.obj"
  
FileStreams.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Common\FileStreams.cpp /Fo"FileStreams.obj"
  
Vector.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Common\Vector.cpp /Fo"Vector.obj"

StringToInt.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Common\StringToInt.cpp /Fo"StringToInt.obj"

StringConvert.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Common\StringConvert.cpp /Fo"StringConvert.obj"

String.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Common\String.cpp /Fo"String.obj"

NewHandler.obj :  $(SRCFILES)
  $(CC) $(LZMACFLAGS)  7zip\Src\Common\NewHandler.cpp /Fo"NewHandler.obj"

CRC.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Common\CRC.cpp /Fo"CRC.obj"

CommandLineParser.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Common\CommandLineParser.cpp /Fo"CommandLineParser.obj"

Alloc.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Common\Alloc.cpp /Fo"Alloc.obj"

FileIO.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\Windows\FileIO.cpp /Fo"FileIO.obj"

LZOutWindow.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Compress\Lz\LZOutWindow.cpp /Fo"LZOutWindow.obj"

LZInWindow.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Compress\Lz\LZInWindow.cpp /Fo"LZInWindow.obj"

RangeCoderBit.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Compress\RangeCoder\RangeCoderBit.cpp /Fo"RangeCoderBit.obj"

LZMAEncoder.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Compress\Lzma\LZMAEncoder.cpp /Fo"LZMAEncoder.obj"

LZMADecoder.obj : $(SRCFILES)
  $(CC) $(LZMACFLAGS) 7zip\Src\7zip\Compress\Lzma\LZMADecoder.cpp /Fo"LZMADecoder.obj"

  
