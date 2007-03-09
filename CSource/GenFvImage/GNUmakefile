ARCH ?= IA32
MAKEROOT ?= ..

APPNAME = GenFvImage

LIBS = -lCommon -lString -L$(CYGWIN_HOME)/lib/e2fsprogs -luuid

OBJECTS = GenFvImageExe.o  GenFvImageLib.o

include $(MAKEROOT)/app.makefile
