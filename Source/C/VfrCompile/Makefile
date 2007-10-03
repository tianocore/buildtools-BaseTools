!INCLUDE ..\MSmakefile.common

APPNAME = VfrCompile

LIBS = Common.lib

OBJECTS = VfrCompile.obj VfrServices.obj DLGLexer.obj EfiVfrParser.obj ATokenBuffer.obj DLexerBase.obj AParser.obj

INC = $(INC) -I $(BASE_TOOLS_PATH)\Source\C\VfrCompile\Pccts\h

!INCLUDE ..\MSmakefile.app

VfrCompile.cpp DLGLexer.cpp EfiVfrParser.cpp: VfrCompile.g
	pushd . & cd Pccts & $(MAKE) & popd
	antlr -CC -e3 -ck 3 -o . VfrCompile.g
	dlg -C2 -i -CC -o . parser.dlg
	pushd . & cd Pccts & $(MAKE) clean

ATokenBuffer.obj: Pccts\h\ATokenBuffer.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

DLexerBase.obj: Pccts\h\DLexerBase.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

AParser.obj: Pccts\h\AParser.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

EXTRA_CLEAN_OBJECTS = EfiVfrParser.cpp parser.dlg EfiVfrParser.h DLGLexer.cpp VfrCompile.cpp tokens.h DLGLexer.h

clean: localClean
cleanall: localClean localCleanall

localClean:
	-DEL $(EXTRA_CLEAN_OBJECTS)

localCleanall:
	pushd . & cd Pccts & $(MAKE) cleanall & popd
