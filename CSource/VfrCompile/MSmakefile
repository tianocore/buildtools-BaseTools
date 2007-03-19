!INCLUDE ..\MSmakefile.common

ARCH = IA32

APPNAME = VfrCompile

LIBS = Common.lib String.lib

OBJECTS = AParser.obj  ATokenBuffer.obj  DLGLexer.obj  DLexerBase.obj  EfiVfrParser.obj  VfrServices.obj VfrCompile.obj

!INCLUDE ..\MSmakefile.app

AParser.cpp:
	copy $(SOURCE_PATH)\Pccts\h\AParser.cpp .

ATokenBuffer.cpp:
	copy $(SOURCE_PATH)\Pccts\h\ATokenBuffer.cpp .

DLexerBase.cpp:
	copy $(SOURCE_PATH)\Pccts\h\DLexerBase.cpp .

DLGLexer.cpp: parser.dlg
	$(BIN_PATH)\dlg -C2 -i -CC -o . parser.dlg

parser.dlg: VfrCompile.g
	$(BIN_PATH)\antlr -CC -e3 -ck 3 -o . VfrCompile.g

CPPFLAGS = $(CPPFLAGS) -I $(SOURCE_PATH)\Pccts\h


