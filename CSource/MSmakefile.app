!INCLUDE MSmakefile.common

APPLICATION = $(BIN_PATH)/$(APPNAME).exe

.PHONY:all
all: $(MAKEROOT)/bin $(APPLOCATION) 

$(APPLICATION): $(OBJECTS) 
	$(LINKER) /nologo /debug /incremental:no /out:$(APPLICATION) /libpath:$(LIB_PATH) $(LIBS) $(OBJECTS)

!INCLUDE MSmakefile.rule

