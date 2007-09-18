ARCH ?= IA32
MAKEROOT ?= ..

APPNAME = GenFvImage

OBJECTS = GenFv.o GenFvInternalLib.o GenFvPadFileTable.o

include $(MAKEROOT)/app.makefile

LIBS = -lCommon
ifeq ($(CYGWIN), CYGWIN)
  LIBS += -L/lib/e2fsprogs -luuid
endif

ifeq ($(LINUX), Linux)
  LIBS += -luuid
endif

