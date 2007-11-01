include $(MAKEROOT)/header.makefile

LIBRARY = $(MAKEROOT)/libs/lib$(LIBNAME).a

all: $(MAKEROOT)/libs $(LIBRARY) 

include $(MAKEROOT)/footer.makefile
