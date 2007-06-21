MAKEROOT ?= ../..

include $(MAKEROOT)/header.makefile

APPLOCATION = $(MAKEROOT)/bin/$(APPNAME)

.PHONY:all
all: $(MAKEROOT)/bin $(APPLOCATION) 

$(APPLOCATION): $(OBJECTS) 
	$(LINKER) -o $(APPLOCATION) $(OBJECTS) -L$(MAKEROOT)/libs $(LIBS)

include $(MAKEROOT)/footer.makefile
