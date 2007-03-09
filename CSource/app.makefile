MAKEROOT ?= ../..

include $(MAKEROOT)/header.makefile

APPLOCATION = $(MAKEROOT)/bin/$(APPNAME)

.PHONY:all
all: $(MAKEROOT)/bin $(APPLOCATION) 

$(APPLOCATION): $(OBJECTS) 
	$(CC) -static -o $(APPLOCATION) $(OBJECTS) -L $(MAKEROOT)/libs -Wl,--start-group $(LIBS) -Wl,--end-group

include $(MAKEROOT)/footer.makefile
