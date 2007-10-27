MAKEROOT ?= ../..

include $(MAKEROOT)/header.makefile

APPLICATION = $(MAKEROOT)/bin/$(APPNAME)

.PHONY:all
all: $(MAKEROOT)/bin $(APPLICATION) 

$(APPLICATION): $(OBJECTS) 
	$(LINKER) -o $(APPLICATION) $(OBJECTS) -L$(MAKEROOT)/libs $(LIBS)

include $(MAKEROOT)/footer.makefile
