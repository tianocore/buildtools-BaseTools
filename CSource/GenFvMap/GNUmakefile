ARCH ?= IA32
MAKEROOT ?= ..

APPNAME = GenFvMap

LIBS = -lCommon -lString

OBJECTS = GenFvMap.o

GenFvMap : $(OBJECTS)
	$(CXX) -o $(APPNAME) $(OBJECTS)

include $(MAKEROOT)/header.makefile
