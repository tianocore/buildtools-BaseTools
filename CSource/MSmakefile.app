!INCLUDE MSmakefile.common

APPLICATION = $(BIN_PATH)\$(APPNAME).exe

.PHONY:all
all: $(APPLOCATION) 

$(APPLICATION): $(OBJECTS) 
	-@if not exist $(BIN_PATH) mkdir $(BIN_PATH)
	$(LINKER) /nologo /debug /incremental:no /out:$(APPLICATION) /libpath:$(LIB_PATH) $(LIBS) $(OBJECTS)

!INCLUDE MSmakefile.rule

