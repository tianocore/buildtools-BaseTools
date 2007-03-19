!INCLUDE MSmakefile.common

APPLICATION = $(BIN_PATH)\$(APPNAME).exe

.PHONY:all
all: $(APPLICATION) 

$(APPLICATION) : $(OBJECTS) 
	-@if not exist $(BIN_PATH) mkdir $(BIN_PATH)
	$(LD) /nologo /debug /incremental:no /out:$@ /libpath:$(LIB_PATH) $(LIBS) $?

!INCLUDE MSmakefile.rule

