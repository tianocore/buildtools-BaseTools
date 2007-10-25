!INCLUDE MSmakefile.common

APPLICATION = $(BIN_PATH)\$(APPNAME).exe

all: $(APPLICATION) 

$(APPLICATION) : $(OBJECTS) 
	-@if not exist $(BIN_PATH) mkdir $(BIN_PATH)
	$(LD) /nologo /debug /incremental:no /nodefaultlib:libc.lib /out:$@ /libpath:$(LIB_PATH) $(LIBS) $**

.PHONY:clean
.PHONY:cleanall

clean:
	del /f /q $(OBJECTS) *.pdb > nul

cleanall:
	del /f /q $(OBJECTS) $(APPLICATION) *.pdb $(BIN_PATH)\*.pdb > nul

!INCLUDE MSmakefile.rule

