ARCH ?= IA32
MAKEROOT ?= ..

LINKER=$(CXX)

VPATH = $(MAKEROOT)/Pccts/h

APPNAME = VfrCompile

LIBS = -lCommon -lString

OBJECTS = AParser.o  ATokenBuffer.o  DLGLexer.o  DLexerBase.o  EfiVfrParser.o  VfrCompile.o  VfrServices.o

include $(MAKEROOT)/app.makefile

DLGLexer.cpp: parser.dlg
	$(MAKEROOT)/bin/dlg -C2 -i -CC -o . parser.dlg

parser.dlg: VfrCompile.g
	$(MAKEROOT)/bin/antlr -CC -e3 -ck 3 -o . VfrCompile.g

CPPFLAGS += -I $(MAKEROOT)/Pccts/h
