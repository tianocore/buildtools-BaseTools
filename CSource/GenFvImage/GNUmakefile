ARCH ?= IA32
MAKEROOT ?= ..

APPNAME = GenFvImage

OBJECTS = GenFvImageExe.o  GenFvImageLib.o

include $(MAKEROOT)/app.makefile

LIBS = -lCommon -lString
ifeq ($(CYGWIN), CYGWIN)
  LIBS += -L/lib/e2fsprogs -luuid
endif

