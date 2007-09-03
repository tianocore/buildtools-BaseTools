!INCLUDE ..\MSmakefile.common

APPNAME = VfrCompile

LIBS = Common.lib

OBJECTS = VfrCompile.obj VfrServices.obj DLGLexer.obj EfiVfrParser.obj ATokenBuffer.obj DLexerBase.obj AParser.obj

INC = $(INC) -I $(BASE_TOOLS_PATH)\Source\C\Pccts\h

!INCLUDE ..\MSmakefile.app

DLGLexer.cpp EfiVfrParser.cpp: VfrCompile.g
	$(MAKE) -f Pccts\Makefile
	antlr -CC -e3 -ck 3 -o . VfrCompile.g
	dlg -C2 -i -CC -o . parser.dlg
	$(MAKE) -f Pccts\Makefile clean

ATokenBuffer.obj: Pccts\h\ATokenBuffer.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

DLexerBase.obj: Pccts\h\DLexerBase.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

AParser.obj: Pccts\h\AParser.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

