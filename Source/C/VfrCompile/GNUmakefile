
ARCH ?= IA32
MAKEROOT ?= ..

APPNAME = VfrCompile

LIBS = -lCommon

TOOL_INCLUDE = -I Pccts/h

OBJECTS = VfrCompile.o VfrServices.o DLGLexer.o EfiVfrParser.o ATokenBuffer.o DLexerBase.o AParser.o

LINKER = $(CXX)

EXTRA_CLEAN_OBJECTS = EfiVfrParser.cpp parser.dlg EfiVfrParser.h DLGLexer.cpp VfrCompile.cpp tokens.h DLGLexer.h

include $(MAKEROOT)/Makefiles/app.makefile

VfrCompile.cpp DLGLexer.cpp EfiVfrParser.cpp: Pccts/antlr/antlr Pccts/dlg/dlg VfrCompile.g
	Pccts/antlr/antlr -CC -e3 -ck 3 -o . VfrCompile.g
	Pccts/dlg/dlg -C2 -i -CC -o . parser.dlg

Pccts/antlr/antlr:
	BIN_DIR='.' make -C Pccts/antlr

Pccts/dlg/dlg:
	BIN_DIR='.' make -C Pccts/dlg

ATokenBuffer.o: Pccts/h/ATokenBuffer.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

DLexerBase.o: Pccts/h/DLexerBase.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

AParser.o: Pccts/h/AParser.cpp
	$(CXX) -c $(CPPFLAGS) $(INC) $? -o $@

clean: localClean

localClean:
	BIN_DIR='.' make -C Pccts/antlr clean
	BIN_DIR='.' make -C Pccts/dlg clean
	rm -f $(EXTRA_CLEAN_OBJECTS)

