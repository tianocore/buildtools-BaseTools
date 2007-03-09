ARCH ?= IA32
MAKEROOT ?= ..

VPATH = $(MAKEROOT)/Pccts/h

APPNAME = VfrCompile

LIBS = -lCommon -lString -lstdc++

OBJECTS = AParser.o  ATokenBuffer.o  DLGLexer.o  DLexerBase.o  EfiVfrParser.o  VfrCompile.o  VfrServices.o

include $(MAKEROOT)/app.makefile

DLGLexer.cpp: parser.dlg
	$(MAKEROOT)/bin/dlg -C2 -i -CC -o . parser.dlg

EfiVfrParser.cpp: VfrCompile.g
	$(MAKEROOT)/bin/antlr -CC -e3 -ck 3 -o . VfrCompile.g

CPPFLAGS += -I $(MAKEROOT)/Pccts/h
